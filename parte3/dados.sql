-- Inserir dados na tabela pessoa
INSERT INTO pessoa (idpessoa, nome, telefone, endereco) VALUES
(1, 'Carlos Silva', '123456789', 'Rua das Flores, 123'),
(2, 'Ana Pereira', '987654321', 'Avenida Central, 456'),
(3, 'João Souza', '555555555', 'Travessa Alegria, 789');

-- Inserir dados na tabela hospede
INSERT INTO hospede (idhospede, idpessoa) VALUES
(1, 1),
(2, 2),
(3, 3);

-- Inserir dados na tabela acompanhante
INSERT INTO acompanhante (idacompanhante, idpessoa, idhospede, nome) VALUES
(1, 1, 2, 'Lucas Pereira'),
(2, 2, 3, 'Fernanda Lima');

-- Inserir dados na tabela quarto
INSERT INTO quarto (codquarto, tipo_quarto, qtdcamas, preco, descricao, frigobar, banheira) VALUES
(101, 'Suite', 1, 150.0, 'Suite com vista para o mar', 'sim', 'não'),
(102, 'Duplo', 2, 100.0, 'Quarto duplo com frigobar', 'sim', 'sim'),
(103, 'Single', 1, 80.0, 'Quarto single com vista para o jardim', 'não', 'não');

-- Inserir dados na tabela reserva
INSERT INTO reserva (idreserva, idhospede, codquarto, estado, datainicio, datafim, valorDesconto) VALUES
(1, 1, 101, 'ativa', '2023-01-10', '2023-01-15', 20.0),
(2, 2, 102, 'ativa', '2023-02-05', '2023-02-10', 15.0),
(3, 3, 103, 'cancelada', '2023-03-01', '2023-03-05', 0.0);

-- Inserir dados na tabela consumo_frigobar
INSERT INTO consumo_frigobar (idconsumo, idreserva, item, quantidade, data) VALUES
(1, 1, 'Água Mineral', 3, '2023-02-08'),
(2, 1, 'Chocolate', 2, '2023-02-09'),
(3, 2, 'Refrigerante', 1, '2023-02-08'),
(4, 3, 'Água Mineral', 4, '2023-03-04');


