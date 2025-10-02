from typing import List, Dict, Any, Optional, Tuple
import re
import unicodedata
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.wine import Wine


def _norm(s: Optional[str]) -> str:
    if not s:
        return ""
    t = unicodedata.normalize("NFKD", s)
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


class WineRecommender:
    async def recommend_wines(self, user_description: str, db: AsyncSession) -> Dict[str, Any]:
        try:
            result = await db.execute(select(Wine))
            wines: List[Wine] = [w for w in result.scalars().all() if getattr(w, "available", True)]

            text = _norm(user_description or "")
            prefs = self._analyze_prefs(text)

            scored: List[Tuple[float, Dict[str, Any]]] = []
            for w in wines:
                s, reasons = self._score_wine(w, prefs)
                item = {
                    "wine": self._wine_payload(w),
                    "score": s,
                    "reasons": reasons,
                }
                scored.append((s, item))

            scored.sort(key=lambda x: x[0], reverse=True)
            # Prefer exact color matches when a color was requested
            if prefs.get("color"):
                color_matches = [item for _, item in scored if self._norm_color(item["wine"].get("color")) == prefs["color"]]
                top = color_matches[:5] if color_matches else [item for _, item in scored[:5]]
            else:
                top = [item for _, item in scored[:5]]

            if not top:
                for w in wines[:3]:
                    top.append({"wine": self._wine_payload(w), "score": 0, "reasons": []})

            explanation = self._build_explanation(prefs, len(wines))

            return {
                "recommendations": top,
                "explanation": explanation,
                "taste_analysis": prefs,
                "total_wines_analyzed": len(wines),
            }
        except Exception as e:
            return {
                "recommendations": [],
                "explanation": "Entschuldigung, bei der Weinempfehlung ist ein Fehler aufgetreten.",
                "error": str(e),
            }

    def _wine_payload(self, w: Wine) -> Dict[str, Any]:
        prices = getattr(w, "prices", {}) or {}
        return {
            "id": getattr(w, "id", None),
            "name": getattr(w, "name", ""),
            "description": getattr(w, "short_description", None) or getattr(w, "long_description", None),
            "price": self._extract_bottle_price(prices),
            "price_bottle": self._extract_bottle_price(prices),
            "price_min": self._extract_min_price(prices),
            "prices": prices,
            "price_labels": self._format_prices_line(prices),
            "color": getattr(w, "color", None),
            "grape": getattr(w, "grape", None),
            "origin": getattr(w, "origin", None),
            "characteristics": getattr(w, "characteristics", None),
            "image_url": getattr(w, "image", None),
            "available": getattr(w, "available", True),
        }

    def _analyze_prefs(self, text: str) -> Dict[str, Any]:
        # text is already normalized (no diacritics, lower-cased)
        color = None
        if re.search(r"\b(rot|tinto|red)\b", text):
            color = "red"
        elif re.search(r"\b(weiss|weisswein|white|blanco)\b", text):
            color = "white"
        elif re.search(r"\b(rose|rosado|rosato|blush)\b", text):
            color = "rose"

        sweetness = None
        if re.search(r"\b(trocken|dry|herb)\b", text):
            sweetness = "trocken"
        elif re.search(r"\b(halb\s*trocken|halbtrocken|semi\s*dry)\b", text):
            sweetness = "halbtrocken"
        elif re.search(r"\b(lieblich|suss|suess|sweet)\b", text):
            sweetness = "suess"

        glass = bool(re.search(r"\b(glas|glasweise|glass|by\s*the\s*glass)\b", text))
        bottle = bool(re.search(r"\b(flasche|bottle)\b", text))

        cheap = bool(re.search(r"\b(gunstig|guenstig|billig|cheap|preiswert)\b", text))

        budget_bottle: Optional[float] = None
        budget_glass: Optional[float] = None
        nums = [float(n.replace(",", ".")) for n in re.findall(r"\d+(?:,\d{1,2})?", text)]
        has_budget_cue = any(k in text for k in [
            "unter", "bis", "max", "maximal", "hoechstens", "hochstens", "budget", "preis", "euro"
        ])
        if nums and (glass or bottle or has_budget_cue):
            if glass:
                budget_glass = min(nums)
            elif bottle:
                budget_bottle = min(nums)
            else:
                budget_bottle = min(nums)

        wants_house = bool(re.search(r"\b(hauswein|haus\s*wein|house\s*w[iy]ne?)\b", text))

        origin_tokens = [
            "spanien",
            "italien",
            "frankreich",
            "deutschland",
            "rioja",
            "ribera",
            "rueda",
            "navarra",
            "alsace",
            "suedtirol",
            "sudtirol",
            "trentin",
        ]
        origins = [tok for tok in origin_tokens if tok in text]

        grape_tokens = [
            "tempranillo",
            "verdejo",
            "garnacha",
            "syrah",
            "merlot",
            "sauvignon",
            "chardonnay",
            "pinot",
        ]
        grapes = [g for g in grape_tokens if g in text]

        return {
            "color": color,
            "sweetness": sweetness,
            "glass": glass,
            "bottle": bottle,
            "budget_bottle": budget_bottle,
            "budget_glass": budget_glass,
            "cheap": cheap,
            "origins": origins,
            "grapes": grapes,
            "wants_house": wants_house,
        }

    def _score_wine(self, w: Wine, prefs: Dict[str, Any]) -> Tuple[float, List[str]]:
        s = 0.0
        reasons: List[str] = []
        color = self._norm_color(getattr(w, "color", None)) or ""
        ch = _norm(getattr(w, "characteristics", ""))
        origin = _norm(getattr(w, "origin", ""))
        grape = _norm(getattr(w, "grape", ""))
        prices = getattr(w, "prices", {}) or {}
        bottle_price = self._extract_bottle_price(prices)
        min_glass = self._extract_min_glass_price(prices)

        if prefs.get("color"):
            if prefs["color"] == color:
                s += 3
                reasons.append({"red": "Rotwein", "white": "Weißwein", "rose": "Rosé"}[color])
            else:
                s -= 1

        sw = prefs.get("sweetness")
        if sw:
            if sw == "trocken" and ("trocken" in ch or "dry" in ch):
                s += 2
                reasons.append("trocken")
            elif sw == "halbtrocken" and ("halbtrocken" in ch or "semi" in ch):
                s += 2
                reasons.append("halbtrocken")
            elif sw == "suess" and ("lieblich" in ch or "suss" in ch or "suess" in ch):
                s += 2
                reasons.append("lieblich/süßer")

        for o in prefs.get("origins", []):
            if o in origin:
                s += 1
                reasons.append(o.title())

        for g in prefs.get("grapes", []):
            if g in grape:
                s += 1
                reasons.append(g)

        if prefs.get("budget_bottle") is not None and bottle_price is not None:
            b = prefs["budget_bottle"]
            if bottle_price <= b:
                s += 2
                reasons.append(f"Flasche ≤ {b:.0f}€")
            elif bottle_price <= b + 3:
                s += 1
                reasons.append(f"nahe {b:.0f}€")
            else:
                s -= 1

        if prefs.get("budget_glass") is not None and min_glass is not None:
            g = prefs["budget_glass"]
            if min_glass <= g:
                s += 2
                reasons.append(f"Glas ≤ {g:.2f}€")
            else:
                s -= 1

        if prefs.get("cheap"):
            if bottle_price is not None:
                s += max(0, 30 - bottle_price) * 0.05
            if min_glass is not None:
                s += max(0, 6 - min_glass) * 0.5

        return s, [str(r) for r in reasons]

    def _build_explanation(self, prefs: Dict[str, Any], total: int) -> str:
        bits: List[str] = []
        if prefs.get("color"):
            bits.append({"red": "Rotwein", "white": "Weißwein", "rose": "Rosé"}[prefs["color"]])
        if prefs.get("sweetness"):
            m = {"trocken": "trocken", "halbtrocken": "halbtrocken", "suess": "lieblich/süß"}
            bits.append(m[prefs["sweetness"]])
        if prefs.get("budget_glass") is not None:
            bits.append(f"Glas bis {prefs['budget_glass']:.2f}€")
        if prefs.get("budget_bottle") is not None:
            bits.append(f"Flasche bis {prefs['budget_bottle']:.0f}€")

        if bits:
            lead = " ".join(bits)
            return f"Dazu passen diese Weine: {lead}."
        return "Hier sind passende Vorschläge. Wenn Sie mir noch Farbe (rot/weiß/rosé), trocken/halbtrocken/süß oder Ihr Budget nennen, treffe ich noch genauer."

    def _extract_bottle_price(self, prices: dict) -> Optional[float]:
        if not prices:
            return None
        val = prices.get("flasche")
        if not val:
            return None
        m = re.search(r"(\d+(?:,\d{2})?)", str(val))
        if m:
            try:
                return float(m.group(1).replace(",", "."))
            except Exception:
                return None
        return None

    def _extract_min_price(self, prices: dict) -> Optional[float]:
        if not prices:
            return None
        vals: List[float] = []
        for v in prices.values():
            if not v:
                continue
            m = re.search(r"(\d+(?:,\d{2})?)", str(v))
            if m:
                try:
                    vals.append(float(m.group(1).replace(",", ".")))
                except Exception:
                    pass
        return min(vals) if vals else None

    def _extract_min_glass_price(self, prices: dict) -> Optional[float]:
        if not prices:
            return None
        keys = ["0.1l", "0.2l", "0.25l", "0.3l", "0.4l", "0.5l", "glas"]
        vals: List[float] = []
        for k in keys:
            if k in prices and prices[k]:
                m = re.search(r"(\d+(?:,\d{2})?)", str(prices[k]))
                if m:
                    try:
                        vals.append(float(m.group(1).replace(",", ".")))
                    except Exception:
                        pass
        return min(vals) if vals else None

    def _format_prices_line(self, prices: dict) -> str:
        if not prices:
            return ""
        def label(k: str) -> str:
            kl = (k or "").lower()
            if kl == "flasche":
                return "Flasche"
            return k.replace(".", ",")
        parts: List[str] = []
        keys = ["0.1l", "0.2l", "0.25l", "0.3l", "0.4l", "0.5l", "glas", "flasche"]
        for k in keys:
            if k in prices:
                parts.append(f"{label(k)} {prices[k]}")
        for k, v in prices.items():
            if k not in keys:
                parts.append(f"{label(k)} {v}")
        return " • ".join(parts)

    def _norm_color(self, c: Optional[str]) -> Optional[str]:
        n = _norm(c or "")
        if not n:
            return None
        # Map common forms robustly, including mis-encoded 'rosÃ©'
        if 'rosso' in n:
            return 'red'
        if any(tok in n for tok in ["rot", "red", "tinto"]):
            return "red"
        if any(tok in n for tok in ["weiss", "weisswein", "white", "blanco"]):
            return "white"
        if any(tok in n for tok in ["rose", "rosado", "rosato", "blush"]) or ("ros" in n and "rosso" not in n):
            return "rose"
        return n