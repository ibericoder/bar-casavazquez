import type {Wine} from "../interfaces/vino.ts";
import {blancos} from "./blancos.ts";
import {rosados} from "./rosados.ts";
import {tintos} from "./tintos.ts";

export const vinos: Wine[] = [
    ...tintos.filter(tinto => tinto.available),
    ...blancos.filter(blanco => blanco.available),
    ...rosados.filter(rosado => rosado.available)
];
