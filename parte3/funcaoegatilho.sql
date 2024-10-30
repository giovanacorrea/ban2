--Trabalho realizado pelas alunas Débora Lawall e Giovana Corrêa 

--Função para calcular custo da reserva
CREATE OR REPLACE FUNCTION calcular_custo_total_reserva(p_idreserva INT)
RETURNS FLOAT AS $$
DECLARE
    preco_quarto FLOAT;
    dias_reserva INT;
    valor_desconto FLOAT;
    custo_frigobar FLOAT := 0;
    custo_total FLOAT;
BEGIN
    SELECT q.preco, r.valorDesconto, (r.dataFim - r.datainicio)
    INTO preco_quarto, valor_desconto, dias_reserva
    FROM reserva r
    JOIN quarto q ON r.codquarto = q.codquarto
    WHERE r.idreserva = p_idreserva;

    SELECT SUM(c.quantidade * 10) INTO custo_frigobar 
    FROM consumo_frigobar c
    WHERE c.idreserva = p_idreserva;

    IF custo_frigobar IS NULL THEN
        custo_frigobar := 0;
    END IF;

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
    SELECT MAX(idcancelamento) INTO v_idcancelamento FROM cancelamento;

    IF v_idcancelamento IS NULL THEN
        v_idcancelamento := 1;
    ELSE
        v_idcancelamento := v_idcancelamento + 1;
    END IF;

    UPDATE reserva
    SET estado = 'Cancelada'
    WHERE idreserva = p_idreserva;

    INSERT INTO cancelamento (idcancelamento, idreserva, dataCancelamento)
    VALUES (v_idcancelamento, p_idreserva, v_dataCancelamento);
END;
$$ LANGUAGE plpgsql;

-- para testar a função 
select calcular_custo_total_reserva(idreserva)
select cancelar_reserva(idreserva)



-- Essa função verifica se a reserva está em um intervalo de datas válidos e caso esteja significa que a reserva está ativa
CREATE OR REPLACE FUNCTION atualizar_estado_reserva()
RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se a data atual está dentro do intervalo da reserva
    IF CURRENT_DATE BETWEEN NEW.datainicio AND NEW.dataFim THEN
        NEW.estado := 'Ativa';
    ELSE
        NEW.estado := 'Inativa';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_atualizar_estado_reserva
BEFORE UPDATE ON reserva
FOR EACH ROW
EXECUTE FUNCTION atualizar_estado_reserva();

-- Verificar o estado após a atualização
SELECT estado FROM reserva WHERE idreserva = 3;


-- Gatilho para verificar disponibilidade de quartos 
CREATE OR REPLACE FUNCTION verificar_disponibilidade_quarto()
RETURNS TRIGGER AS $$
DECLARE
    v_contagem INT;
BEGIN
    SELECT COUNT(*)
    INTO v_contagem
    FROM reserva
    WHERE codquarto = NEW.codquarto
      AND estado <> 'Cancelada'  
      AND (
          (NEW.datainicio BETWEEN datainicio AND dataFim) OR
          (NEW.dataFim BETWEEN datainicio AND dataFim) OR
          (datainicio BETWEEN NEW.datainicio AND NEW.dataFim)
      );

    IF v_contagem > 0 THEN
        RAISE EXCEPTION 'O quarto % não está disponível nas datas informadas.', NEW.codquarto;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS trg_verificar_disponibilidade ON reserva;

CREATE TRIGGER trg_verificar_disponibilidade
BEFORE INSERT ON reserva
FOR EACH ROW
EXECUTE FUNCTION verificar_disponibilidade_quarto();