import type {Wine} from "../interfaces/vino.ts";
import {blancos} from "../../../data/blancos";
import {rosados} from "../../../data/rosados";
import {tintos} from "../../../data/tintos";

export const vinos: Wine[] = [
    ...tintos.filter(tinto => tinto.available),
    ...blancos.filter(blanco => blanco.available),
    ...rosados.filter(rosado => rosado.available)
];
