
--MODELO RELACIONAL

--CRIANDO TABELA Endereco
CREATE TABLE Endereco (
    idEndereco INTEGER PRIMARY KEY AUTOINCREMENT,
    paisCliente VARCHAR(40),
    estadoCliente VARCHAR(40),
    cidadeCliente VARCHAR(40)
);

--CRIANDO TABELA Cliente

CREATE TABLE Cliente (
    idCliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nomeCliente VARCHAR(100),
    idEndereco INT,
    FOREIGN KEY (idEndereco) REFERENCES Endereco(idEndereco)
);

--CRIANDO TABELA Vendedor

CREATE TABLE Vendedor (
    idVendedor INTEGER PRIMARY KEY AUTOINCREMENT,
    nomeVendedor VARCHAR(15),
    sexoVendedor SMALLINT,
    estadoVendedor VARCHAR(40)
);

--CRIANDO TABELA Combustivel

CREATE TABLE Combustivel (
    idCombustivel INTEGER PRIMARY KEY AUTOINCREMENT,
    tipoCombustivel VARCHAR(20)
);

--CRIANDO TABELA Carro

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

--CRIANDO TABELA Locacao

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




   
--MODELO DIMENSIONAL


--DIMENSÃO CARRO

CREATE VIEW dim_carro AS
SELECT carro.idCarro,
       carro.kmCarro,
       carro.chassiCarro,
       carro.marcaCarro,
       carro.modeloCarro,
       carro.anoCarro,
       combustivel.tipoCombustivel
FROM Carro carro
JOIN Combustivel combustivel ON carro.idCombustivel = combustivel.idCombustivel;

--DIMENSÃO VENDEDOR

CREATE VIEW dim_vendedor AS
SELECT vendedor.idVendedor,
       vendedor.nomeVendedor,
       vendedor.sexoVendedor,
       vendedor.estadoVendedor
FROM vendedor;

--DIMENSÃO CLIENTE

CREATE VIEW dim_cliente AS
SELECT cliente.idCliente,
       cliente.nomeCliente,
       endereco.cidadeCliente,
       endereco.estadoCliente,
       endereco.paisCliente
FROM cliente
JOIN endereco ON cliente.idEndereco = endereco.idEndereco;

--DIMENSÃO data_e_hora_locacao

CREATE VIEW dim_data_e_hora_locacao AS
SELECT DISTINCT
       CONCAT(dataLocacao, ' ', horaLocacao) AS dtHrLocacao,
       SUBSTR(dataLocacao, 1, 4) AS ano,
       SUBSTR(dataLocacao, 5, 2) AS mes,
       SUBSTR(dataLocacao, 7, 2) AS dia,
  	   strftime('%H', printf('%02d:%02d', CAST(substr(horaLocacao, 1, instr(horaLocacao, ':') - 1) AS INTEGER), CAST(substr(horaLocacao, instr(horaLocacao, ':') + 1) AS INTEGER))) AS hora,
       strftime('%M', printf('%02d:%02d', CAST(substr(horaLocacao, 1, instr(horaLocacao, ':') - 1) AS INTEGER), CAST(substr(horaLocacao, instr(horaLocacao, ':') + 1) AS INTEGER))) AS minutos
FROM locacao;

--DIMENSÃO data_e_hora_entrega

CREATE VIEW dim_data_e_hora_entrega AS
SELECT DISTINCT
       CONCAT(dataEntrega, ' ', horaEntrega) AS dtHrEntrega,
       SUBSTR(dataEntrega, 1, 4) AS ano,
       SUBSTR(dataEntrega, 5, 2) AS mes,
       SUBSTR(dataEntrega, 7, 2) AS dia,
   	   strftime('%H', printf('%02d:%02d', CAST(substr(horaEntrega, 1, instr(horaEntrega, ':') - 1) AS INTEGER), CAST(substr(horaEntrega, instr(horaEntrega, ':') + 1) AS INTEGER))) AS hora,
       strftime('%M', printf('%02d:%02d', CAST(substr(horaEntrega, 1, instr(horaEntrega, ':') - 1) AS INTEGER), CAST(substr(horaEntrega, instr(horaEntrega, ':') + 1) AS INTEGER))) AS minutos
FROM locacao;

--Tabela fato locacao

CREATE VIEW fato_locacao AS
SELECT idLocacao,
       qtdDiaria,
       idCliente,
       idVendedor,
       idCarro,
       CONCAT(dataLocacao, ' ', horaLocacao) AS dtHrLocacao,
       CONCAT(dataEntrega, ' ', horaEntrega) AS dtHrEntrega
FROM locacao;

