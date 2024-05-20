--MIGRAÇÃO DOS DADOS DE tb_locacao




--Inserção de Endeco

INSERT INTO Endereco (paisCliente, estadoCliente, cidadeCliente)
SELECT DISTINCT paisCliente, estadoCliente, cidadeCliente
FROM tb_locacao;

--inserção de Cliente

INSERT INTO Cliente (idCliente, nomeCliente, idEndereco)
SELECT DISTINCT t.idCliente, t.nomeCliente, e.idEndereco
FROM tb_locacao t
JOIN Endereco e ON t.paisCliente = e.paisCliente AND t.estadoCliente = e.estadoCliente AND t.cidadeCliente = e.cidadeCliente;

--Inserção de Vendedor

INSERT INTO Vendedor (idVendedor, nomeVendedor, sexoVendedor, estadoVendedor)
SELECT DISTINCT idVendedor, nomeVendedor, sexoVendedor, estadoVendedor
FROM tb_locacao;

--Inserção de Combustivel

INSERT INTO Combustivel (idCombustivel, tipoCombustivel)
SELECT DISTINCT idCombustivel, tipoCombustivel
FROM tb_locacao;

--Inserção de carro

INSERT INTO Carro (idCarro, kmCarro, chassiCarro, marcaCarro, modeloCarro, anoCarro, idCombustivel)
SELECT idCarro, kmCarro, classiCarro, marcaCarro, modeloCarro, anoCarro, idCombustivel
FROM tb_locacao AS t1
WHERE kmCarro = (
    SELECT MAX(kmCarro)
    FROM tb_locacao AS t2
    WHERE t2.classiCarro = t1.classiCarro
      AND t2.idCarro = t1.idCarro
      AND t2.marcaCarro = t1.marcaCarro
      AND t2.modeloCarro = t1.modeloCarro
      AND t2.anoCarro = t1.anoCarro
);

--Inserção de locação

INSERT INTO Locacao (idLocacao, idCliente, idCarro, idVendedor, dataLocacao, horaLocacao, qtdDiaria, vlrDiaria, dataEntrega, horaEntrega)
SELECT t.idLocacao , cl.idCliente, ca.idCarro, v.idVendedor, t.dataLocacao, t.horaLocacao, t.qtdDiaria, t.vlrDiaria, t.dataEntrega, t.horaEntrega
FROM tb_locacao t
LEFT JOIN Cliente cl ON t.idCliente  = cl.idCliente 
JOIN Carro ca ON t.idCarro  = ca.idCarro 
JOIN Vendedor v ON t.idVendedor  = v.idVendedor ;


--Deleção de tb_locação

DROP TABLE tb_locacao;
