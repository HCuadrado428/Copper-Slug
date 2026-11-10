package com.copperslug.armas;

/**
 * De DanoArma de Miscelánea solo queda la marca: true mientras un arma aplica una parte extra de su golpe (para que
 * nada lo cuente como un golpe nuevo). El reparto de daño de las armas de fuego lo hace cada una (Balistica, etc.).
 */
public final class DanoArma {
    private DanoArma() {}

    public static boolean extra;
}
