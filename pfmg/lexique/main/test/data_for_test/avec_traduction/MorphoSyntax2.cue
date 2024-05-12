//contractions:
//  au: [ "à", "le" ]
//  aux: [ "à", "les" ]
//  du: [ "de", "le" ]
//  Des: [ "de", "les" ]
//  Katisha: ["", "Katisha"]
//  Katishas: ["", "Katishas"]
//start: "NP"
//syntagmes:
//  NP:
//    - [ "DET/?", "ADJ/?", "ADJ/?", "N", "ADJ/?" ]
//    - [ "DET2", "NNP" ]
//accords:
//  NP:
//    - [ { sGenre: "*", sNombre: "*", dGenre: "*", dNombre: "*", dCas: "*" },
//        { sGenre: "*", sNombre: "*", dGenre: "*", dNombre: "*" },
//        { sGenre: "*", sNombre: "*", dGenre: "*", dNombre: "*" },
//        { sGenre: "*", sNombre: "*", dGenre: "*", dNombre: "*", dCas: "*" },
//        { sGenre: "*", sNombre: "*", dGenre: "*", dNombre: "*" } ]
//    - [ { sGenre: "*", sNombre: "*", dNombre: "*", dCas: "*" },
//        { sGenre: "*", sNombre: "*", dNombre: "*", dCas: "*" } ]
//percolations:
//  NP:
//    - { sGenre: "*", sNombre: "*",
//        dGenre: "*", dNombre: "*", dCas: "*" }
//    - { sGenre: "*", sNombre: "*",
//        dGenre: "*", dNombre: "*", dCas: "*" }
//traductions:
//  NP:
//    - [ 0, 3, 1, 2, 4 ]
//    - [ 0, 1 ]
