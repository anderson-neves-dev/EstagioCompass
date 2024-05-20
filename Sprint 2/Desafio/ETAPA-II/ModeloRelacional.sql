
--MODELO RELACIONAL

CREATE TABLE Endereco (
    idEndereco INTEGER PRIMARY KEY AUTOINCREMENT,
    paisCliente VARCHAR(40),
    estadoCliente VARCHAR(40),
    cidadeCliente VARCHAR(40)
);

CREATE TABLE Cliente (
    idCliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nomeCliente VARCHAR(100),
    idEndereco INT,
    FOREIGN KEY (idEndereco) REFERENCES Endereco(idEndereco)
);

CREATE TABLE Vendedor (
    idVendedor INTEGER PRIMARY KEY AUTOINCREMENT,
    nomeVendedor VARCHAR(15),
    sexoVendedor SMALLINT,
    estadoVendedor VARCHAR(40)
);

CREATE TABLE Combustivel (
    idCombustivel INTEGER PRIMARY KEY AUTOINCREMENT,
    tipoCombustivel VARCHAR(20)
);

CREATE TABLE Carro (
    idCarro INTEGER PRIMARY KEY AUTOINCREMENT,
    kmCarro INT,
    chassiCarro VARCHAR(50),
    marcaCarro VARCHAR(80),
    modeloCarro VARCHAR(80),
    anoCarro INT,
    idCombustivel INTEGER,
    FOREIGN KEY (idCombustivel) REFERENCES Combustivel(idCombustivel)
);


CREATE TABLE Locacao (
    idLocacao INTEGER PRIMARY KEY AUTOINCREMENT,
    idCliente INT,
    idCarro INT,
    idVendedor INT,
    dataLocacao DATE,
    horaLocacao TIME,
    qtdDiaria INT,
    vlrDiaria DECIMAL(18,2),
    dataEntrega DATE,
    horaEntrega TIME,
    FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente),
    FOREIGN KEY (idCarro) REFERENCES Carro(idCarro),
    FOREIGN KEY (idVendedor) REFERENCES Vendedor(idVendedor)
);
