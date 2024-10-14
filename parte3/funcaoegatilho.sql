--Função para calcular custo da reserva

CREATE OR REPLACE FUNCTION calcular_custo_total_reserva(p_idreserva INT)
RETURNS FLOAT AS $$
DECLARE
    preco_quarto FLOAT;
    dias_reserva INT;
    valor_desconto FLOAT;
    custo_frigobar FLOAT := 0; -- Inicializando como 0
    custo_total FLOAT;
BEGIN
    -- Obter o preço do quarto, o desconto e a duração da estadia
    SELECT q.preco, r.valorDesconto, (r.dataFim - r.datainicio)
    INTO preco_quarto, valor_desconto, dias_reserva
    FROM reserva r
    JOIN quarto q ON r.codquarto = q.codquarto
    WHERE r.idreserva = p_idreserva;

    -- Calcular o custo do consumo do frigobar para esta reserva
    SELECT SUM(c.quantidade * 10) INTO custo_frigobar -- Assumindo que cada item custa 10
    FROM consumo_frigobar c
    WHERE c.idreserva = p_idreserva;

    -- Verificar se o custo do frigobar é nulo e definir como 0 se for o caso
    IF custo_frigobar IS NULL THEN
        custo_frigobar := 0;
    END IF;

    -- Calcular o custo total
    custo_total := (preco_quarto * dias_reserva) - valor_desconto + custo_frigobar;

    RETURN custo_total;
END;
$$ LANGUAGE plpgsql;

-- Função Cancelar reserva
CREATE OR REPLACE FUNCTION cancelar_reserva(p_idreserva INT)
RETURNS VOID AS $$
DECLARE
    v_dataCancelamento DATE := CURRENT_DATE;
    v_idcancelamento INT;
BEGIN
    -- Calcular o próximo valor para idcancelamento
    SELECT MAX(idcancelamento) INTO v_idcancelamento FROM cancelamento;

    -- Se o valor for nulo, significa que a tabela está vazia, então começamos com 1
    IF v_idcancelamento IS NULL THEN
        v_idcancelamento := 1;
    ELSE
        v_idcancelamento := v_idcancelamento + 1;
    END IF;

    -- Atualizar o status da reserva
    UPDATE reserva
    SET estado = 'Cancelada'
    WHERE idreserva = p_idreserva;

    -- Inserir o registro de cancelamento
    INSERT INTO cancelamento (idcancelamento, idreserva, dataCancelamento)
    VALUES (v_idcancelamento, p_idreserva, v_dataCancelamento);
END;
$$ LANGUAGE plpgsql;


-- Dados utilizados para testar a função 
INSERT INTO pessoa (idpessoa, nome, telefone, endereco) VALUES (2, 'Giovana', '111111111', 'Rua A, 123');
INSERT INTO hospede (idhospede, idpessoa) VALUES (2, 2);
INSERT INTO quarto (codquarto, tipo_quarto, qtdcamas, preco, descricao, frigobar, banheira) 
VALUES (102, 'Luxo', 2, 200.00, 'Quarto com vista para o mar', 'Sim', 'Sim');

-- Insira uma reserva para o teste
INSERT INTO reserva (idreserva, idhospede, codquarto, estado, datainicio, dataFim, valorDesconto) 
VALUES (3, 2, 102, 'Ativa', '2024-10-10', '2024-10-15', 50.00);

-- Agora insira o consumo do frigobar
INSERT INTO consumo_frigobar (idconsumo, idreserva, item, quantidade, data) 
VALUES (2, 3, 'Cerveja', 2, '2024-10-11');


-- criando a reserva 
INSERT INTO reserva (idreserva, idhospede, codquarto, estado, datainicio, dataFim, valorDesconto) 
VALUES (2, 1, 101, 'Ativa', '2024-11-01', '2024-11-05', 0.00);

-- para testar a função 
select calcular_custo_total_reserva(idreserva)
select cancelar_reserva(idreserva)