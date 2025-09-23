

//////////////// TENTATIVA 3
    
//PROCESO 1

estado[0] = true;
while(estado[1]){
    // no hacer nada
}
// SECCION CRITRICA
estado[0] = false;    



//PROCESO 2

estado[1] = true;
while(estado[0]){
    // no hacer nada
}
// SECCION CRITRICA
estado[1] = false;    


//////////////// TENTATIVA 4


//PROCESO 1

estado[0] = true;
while(estado[1]){
    estado[0] = false;
    //restraso
    estado[0] = true;
}
// * SECCION CRITRICA *
estado[0] = false;    

//PROCESO 2

estado[1] = true;
while(estado[0]){
    estado[1] = false;
    //restraso
    estado[1] = true;
}
// * SECCION CRITRICA *
estado[1] = false; 



//////////////////////////////////// ALGORITMO DECKER /////////////////////////////
bool estado[2];
int turno;

void P0() {
    while (true) {
        estado[0] = true;
        while (estado[1]) {
            if (turno == 1) {
                estado[0] = false;
                while (turno == 1) {
                    /* no hacer nada */;
                }
                estado[0] = true;
            }
        }

        /* sección crítica */

        turno = 1;
        estado[0] = false;

        /* resto */
    }
}

void P1() {
    while (true) {
        estado[1] = true;
        while (estado[0]) {
            if (turno == 0) {
                estado[1] = false;
                while (turno == 0) {
                    /* no hacer nada */;
                }
                estado[1] = true;
            }
        }

        /* sección crítica */

        turno = 0;
        estado[1] = false;

        /* resto */
    }
}

void main() {
    estado[0] = false;
    estado[1] = false;
    turno = 1;
    paralelos(P0,P1);
}
