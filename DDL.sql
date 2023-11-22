drop table TB_IC_TESTE cascade constraints;
drop table TB_IC_TESTE_LOG cascade constraints;

CREATE TABLE TB_IC_TESTE (
    id_teste            NUMERIC,
    nome                VARCHAR2(150),
    objetivo            VARCHAR2(250),
    ind_funcional       VARCHAR2(250),
    preparacao          VARCHAR2(250),
    dados_input         VARCHAR2(250),
    dados_output        VARCHAR2(250),
    desc_procedimento   VARCHAR2(250)
);

ALTER TABLE TB_IC_TESTE
ADD CONSTRAINT PK_TB_IC_TESTE PRIMARY KEY (id_teste);

CREATE SEQUENCE  SEQ_TB_IC_TESTE  INCREMENT BY 1 START WITH 1;

CREATE TABLE TB_IC_TESTE_LOG (
    id_log          NUMERIC,
    id_teste        NUMERIC,
    responsavel     VARCHAR2(100),
    dt_hora_exec    DATE,
    resultado       VARCHAR2(50),
    obs_falha       VARCHAR2(150)
);

ALTER TABLE TB_IC_TESTE_LOG
ADD CONSTRAINT PK_TB_IC_TESTE_LOG PRIMARY KEY (id_log);

CREATE SEQUENCE  SEQTB_IC_TESTE_LOG  INCREMENT BY 1 START WITH 1;

ALTER TABLE TB_IC_TESTE_LOG
ADD CONSTRAINT FK_TB_IC_TESTE_LOG
FOREIGN KEY (id_teste) REFERENCES TB_IC_TESTE(id_teste);


INSERT INTO TB_IC_TESTE_LOG (id_log, id_teste, responsavel, dt_hora_exec, resultado, obs_falha)
VALUES(SEQTB_IC_TESTE_LOG.NEXTVAL, 2, 'Vinicius', TO_DATE('20/11/2023 16:13:15', 'DD/MM/YYYY HH24:MI:SS'), 'SUCESSO', '');