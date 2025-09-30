import type {Wine} from "./vino";
import {blancos} from "./blancos";
import {rosados} from "./rosados";
import {tintos} from "./tintos";

export const vinos: Wine[] = [
    ...tintos.filter(tinto => tinto.available),
    ...blancos.filter(blanco => blanco.available),
    ...rosados.filter(rosado => rosado.available)
];
