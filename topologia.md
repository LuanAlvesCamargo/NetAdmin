# Topologia 01:

```
{
    "nodes": [
        {"id": "Core", "type": "router"},
        {"id": "R1", "type": "router"},
        {"id": "R2", "type": "router"},
        {"id": "R3", "type": "router"},
        {"id": "Server", "type": "server"},
        {"id": "User1", "type": "user"},
        {"id": "User2", "type": "user"},
        {"id": "User3", "type": "user"},
        {"id": "User4", "type": "user"}
    ],
    "edges": [
        {"source": "Core", "target": "R1", "weight": 2},
        {"source": "Core", "target": "R2", "weight": 4},
        {"source": "R1", "target": "R3", "weight": 3},
        {"source": "R2", "target": "Server", "weight": 5},
        {"source": "R3", "target": "User1", "weight": 2},
        {"source": "R3", "target": "User2", "weight": 3},
        {"source": "R2", "target": "User3", "weight": 2},
        {"source": "R2", "target": "User4", "weight": 4}
    ]
}
```

# Topologia 02

```
{
    "nodes": [

        { "id": "CoreCampus", "type": "router" },

        { "id": "R-Administracao", "type": "router" },
        { "id": "R-Biblioteca", "type": "router" },
        { "id": "R-Laboratorios", "type": "router" },
        { "id": "R-SalasAula", "type": "router" },
        { "id": "R-WifiCampus", "type": "router" },

        { "id": "SW-ADM-01", "type": "switch" },
        { "id": "SW-ADM-02", "type": "switch" },

        { "id": "SW-BIB-01", "type": "switch" },

        { "id": "SW-LAB-01", "type": "switch" },
        { "id": "SW-LAB-02", "type": "switch" },

        { "id": "SW-SALA-01", "type": "switch" },
        { "id": "SW-SALA-02", "type": "switch" },

        { "id": "SW-WIFI-01", "type": "switch" },
        { "id": "SW-WIFI-02", "type": "switch" },

        { "id": "Server-Academico", "type": "server" },
        { "id": "Server-Moodle", "type": "server" },
        { "id": "Server-Arquivos", "type": "server" },
        { "id": "Server-Backup", "type": "server" },

        { "id": "Aluno01", "type": "user" },
        { "id": "Aluno02", "type": "user" },
        { "id": "Aluno03", "type": "user" },
        { "id": "Aluno04", "type": "user" },
        { "id": "Aluno05", "type": "user" },
        { "id": "Aluno06", "type": "user" },

        { "id": "Professor01", "type": "user" },
        { "id": "Professor02", "type": "user" },

        { "id": "Secretaria01", "type": "user" },
        { "id": "Secretaria02", "type": "user" },

        { "id": "LabPC01", "type": "user" },
        { "id": "LabPC02", "type": "user" },
        { "id": "LabPC03", "type": "user" },
        { "id": "LabPC04", "type": "user" },

        { "id": "WifiUser01", "type": "user" },
        { "id": "WifiUser02", "type": "user" },
        { "id": "WifiUser03", "type": "user" },
        { "id": "WifiUser04", "type": "user" }

    ],

    "edges": [

        { "source": "CoreCampus", "target": "R-Administracao", "weight": 1 },
        { "source": "CoreCampus", "target": "R-Biblioteca", "weight": 1 },
        { "source": "CoreCampus", "target": "R-Laboratorios", "weight": 2 },
        { "source": "CoreCampus", "target": "R-SalasAula", "weight": 2 },
        { "source": "CoreCampus", "target": "R-WifiCampus", "weight": 1 },

        { "source": "CoreCampus", "target": "Server-Academico", "weight": 1 },
        { "source": "CoreCampus", "target": "Server-Moodle", "weight": 2 },
        { "source": "CoreCampus", "target": "Server-Arquivos", "weight": 2 },
        { "source": "CoreCampus", "target": "Server-Backup", "weight": 3 },

        { "source": "R-Administracao", "target": "SW-ADM-01", "weight": 1 },
        { "source": "R-Administracao", "target": "SW-ADM-02", "weight": 1 },

        { "source": "R-Biblioteca", "target": "SW-BIB-01", "weight": 1 },

        { "source": "R-Laboratorios", "target": "SW-LAB-01", "weight": 1 },
        { "source": "R-Laboratorios", "target": "SW-LAB-02", "weight": 2 },

        { "source": "R-SalasAula", "target": "SW-SALA-01", "weight": 1 },
        { "source": "R-SalasAula", "target": "SW-SALA-02", "weight": 1 },

        { "source": "R-WifiCampus", "target": "SW-WIFI-01", "weight": 1 },
        { "source": "R-WifiCampus", "target": "SW-WIFI-02", "weight": 2 },

        { "source": "SW-SALA-01", "target": "Aluno01", "weight": 1 },
        { "source": "SW-SALA-01", "target": "Aluno02", "weight": 1 },

        { "source": "SW-SALA-02", "target": "Aluno03", "weight": 1 },
        { "source": "SW-SALA-02", "target": "Aluno04", "weight": 1 },

        { "source": "SW-BIB-01", "target": "Aluno05", "weight": 1 },
        { "source": "SW-BIB-01", "target": "Aluno06", "weight": 1 },

        { "source": "SW-ADM-01", "target": "Secretaria01", "weight": 1 },
        { "source": "SW-ADM-02", "target": "Secretaria02", "weight": 1 },

        { "source": "SW-ADM-01", "target": "Professor01", "weight": 1 },
        { "source": "SW-ADM-02", "target": "Professor02", "weight": 1 },

        { "source": "SW-LAB-01", "target": "LabPC01", "weight": 1 },
        { "source": "SW-LAB-01", "target": "LabPC02", "weight": 1 },

        { "source": "SW-LAB-02", "target": "LabPC03", "weight": 1 },
        { "source": "SW-LAB-02", "target": "LabPC04", "weight": 1 },

        { "source": "SW-WIFI-01", "target": "WifiUser01", "weight": 1 },
        { "source": "SW-WIFI-01", "target": "WifiUser02", "weight": 1 },

        { "source": "SW-WIFI-02", "target": "WifiUser03", "weight": 2 },
        { "source": "SW-WIFI-02", "target": "WifiUser04", "weight": 2 }

    ]
}

```

# Topologia 03

````
{
    "nodes": [

        { "id": "Core1", "type": "router" },
        { "id": "Core2", "type": "router" },

        { "id": "R1", "type": "router" },
        { "id": "R2", "type": "router" },
        { "id": "R3", "type": "router" },
        { "id": "R4", "type": "router" },
        { "id": "R5", "type": "router" },
        { "id": "R6", "type": "router" },

        { "id": "SW1", "type": "switch" },
        { "id": "SW2", "type": "switch" },
        { "id": "SW3", "type": "switch" },
        { "id": "SW4", "type": "switch" },
        { "id": "SW5", "type": "switch" },
        { "id": "SW6", "type": "switch" },
        { "id": "SW7", "type": "switch" },
        { "id": "SW8", "type": "switch" },

        { "id": "ServerAuth", "type": "server" },
        { "id": "ServerDB", "type": "server" },
        { "id": "ServerFiles", "type": "server" },
        { "id": "ServerBackup", "type": "server" },
        { "id": "ServerWeb", "type": "server" },

        { "id": "User01", "type": "user" },
        { "id": "User02", "type": "user" },
        { "id": "User03", "type": "user" },
        { "id": "User04", "type": "user" },
        { "id": "User05", "type": "user" },
        { "id": "User06", "type": "user" },
        { "id": "User07", "type": "user" },
        { "id": "User08", "type": "user" },
        { "id": "User09", "type": "user" },
        { "id": "User10", "type": "user" },

        { "id": "User11", "type": "user" },
        { "id": "User12", "type": "user" },
        { "id": "User13", "type": "user" },
        { "id": "User14", "type": "user" },
        { "id": "User15", "type": "user" },
        { "id": "User16", "type": "user" },
        { "id": "User17", "type": "user" },
        { "id": "User18", "type": "user" },
        { "id": "User19", "type": "user" },
        { "id": "User20", "type": "user" }

    ],

    "edges": [

        { "source": "Core1", "target": "Core2", "weight": 1 },

        { "source": "Core1", "target": "ServerAuth", "weight": 1 },
        { "source": "Core1", "target": "ServerDB", "weight": 2 },
        { "source": "Core2", "target": "ServerFiles", "weight": 2 },
        { "source": "Core2", "target": "ServerBackup", "weight": 3 },
        { "source": "Core2", "target": "ServerWeb", "weight": 1 },

        { "source": "Core1", "target": "R1", "weight": 1 },
        { "source": "Core1", "target": "R2", "weight": 2 },
        { "source": "Core2", "target": "R3", "weight": 2 },
        { "source": "Core2", "target": "R4", "weight": 1 },
        { "source": "Core2", "target": "R5", "weight": 3 },
        { "source": "Core1", "target": "R6", "weight": 2 },

        { "source": "R1", "target": "SW1", "weight": 1 },
        { "source": "R1", "target": "SW2", "weight": 1 },

        { "source": "R2", "target": "SW3", "weight": 1 },
        { "source": "R2", "target": "SW4", "weight": 2 },

        { "source": "R3", "target": "SW5", "weight": 1 },
        { "source": "R4", "target": "SW6", "weight": 2 },

        { "source": "R5", "target": "SW7", "weight": 1 },
        { "source": "R6", "target": "SW8", "weight": 2 },

        { "source": "SW1", "target": "User01", "weight": 1 },
        { "source": "SW1", "target": "User02", "weight": 1 },
        { "source": "SW1", "target": "User03", "weight": 1 },

        { "source": "SW2", "target": "User04", "weight": 1 },
        { "source": "SW2", "target": "User05", "weight": 1 },

        { "source": "SW3", "target": "User06", "weight": 2 },
        { "source": "SW3", "target": "User07", "weight": 2 },

        { "source": "SW4", "target": "User08", "weight": 1 },
        { "source": "SW4", "target": "User09", "weight": 1 },

        { "source": "SW5", "target": "User10", "weight": 1 },
        { "source": "SW5", "target": "User11", "weight": 2 },

        { "source": "SW6", "target": "User12", "weight": 1 },
        { "source": "SW6", "target": "User13", "weight": 1 },

        { "source": "SW7", "target": "User14", "weight": 2 },
        { "source": "SW7", "target": "User15", "weight": 2 },

        { "source": "SW8", "target": "User16", "weight": 1 },
        { "source": "SW8", "target": "User17", "weight": 1 },
        { "source": "SW8", "target": "User18", "weight": 2 },
        { "source": "SW8", "target": "User19", "weight": 2 },
        { "source": "SW8", "target": "User20", "weight": 3 }

    ]
}```
`
````
