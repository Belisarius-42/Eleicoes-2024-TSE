WITH tb_cand AS (
    SELECT 
        SQ_CANDIDATO,
        SG_UF,
        DS_CARGO,
        SG_PARTIDO, 
        NM_PARTIDO,
        DT_NASCIMENTO,
        DS_GENERO, 
        DS_GRAU_INSTRUCAO,
        DS_ESTADO_CIVIL,
        DS_COR_RACA,
        NR_TURNO,
        DS_OCUPACAO,
        DS_SIT_TOT_TURNO
    FROM tb_candidaturas
),

total_bens AS (
    SELECT 
        SQ_CANDIDATO,
        SUM(VR_BEM_CANDIDATO) AS bens 
    FROM tb_bens
    GROUP BY SQ_CANDIDATO
),

tb_completa AS (
    SELECT 
        t1.*, 
        COALESCE(t2.bens, 0) AS totalBens
    FROM tb_cand t1
    LEFT JOIN total_bens t2 
        ON t1.SQ_CANDIDATO = t2.SQ_CANDIDATO
),

 partidos_ideologia AS (
    SELECT 'PARTIDO DOS TRABALHADORES' AS NM_PARTIDO, 'ESQUERDA' AS IDEOLOGIA
    UNION ALL SELECT 'AGIR', 'CENTRO'
    UNION ALL SELECT 'AVANTE', 'CENTRO'
    UNION ALL SELECT 'CIDADANIA', 'CENTRO'
    UNION ALL SELECT 'DEMOCRACIA CRISTÃ', 'CENTRO-DIREITA'
    UNION ALL SELECT 'MOBILIZAÇÃO NACIONAL', 'ESQUERDA'
    UNION ALL SELECT 'MOVIMENTO DEMOCRÁTICO BRASILEIRO', 'CENTRO'
    UNION ALL SELECT 'PARTIDO COMUNISTA BRASILEIRO', 'EXTREMA-ESQUERDA'
    UNION ALL SELECT 'PARTIDO COMUNISTA DO BRASIL', 'EXTREMA-ESQUERDA'
    UNION ALL SELECT 'PARTIDO DA CAUSA OPERÁRIA', 'EXTREMA-ESQUERDA'
    UNION ALL SELECT 'PARTIDO DA MULHER BRASILEIRA', 'CENTRO-DIREITA'
    UNION ALL SELECT 'PARTIDO DA SOCIAL DEMOCRACIA BRASILEIRA', 'CENTRO-DIREITA'
    UNION ALL SELECT 'PARTIDO DEMOCRÁTICO TRABALHISTA', 'ESQUERDA'
    UNION ALL SELECT 'PARTIDO LIBERAL', 'DIREITA'
    UNION ALL SELECT 'PARTIDO NOVO', 'DIREITA'
    UNION ALL SELECT 'PARTIDO RENOVAÇÃO DEMOCRÁTICA', 'CENTRO-ESQUERDA'
    UNION ALL SELECT 'PARTIDO SOCIAL DEMOCRÁTICO', 'CENTRO'
    UNION ALL SELECT 'PARTIDO RENOVADOR TRABALHISTA BRASILEIRO', 'CENTRO-ESQUERDA'
    UNION ALL SELECT 'PARTIDO SOCIALISMO E LIBERDADE', 'ESQUERDA'
    UNION ALL SELECT 'PARTIDO SOCIALISTA BRASILEIRO', 'CENTRO-ESQUERDA'
    UNION ALL SELECT 'PARTIDO SOCIALISTA DOS TRABALHADORES UNIFICADO', 'EXTREMA-ESQUERDA'
    UNION ALL SELECT 'PARTIDO VERDE', 'CENTRO-ESQUERDA'
    UNION ALL SELECT 'PODEMOS', 'DIREITA'
    UNION ALL SELECT 'PROGRESSISTAS', 'CENTRO-DIREITA'
    UNION ALL SELECT 'REDE SUSTENTABILIDADE', 'CENTRO-ESQUERDA'
    UNION ALL SELECT 'REPUBLICANOS', 'CENTRO-DIREITA'
    UNION ALL SELECT 'SOLIDARIEDADE', 'CENTRO'
    UNION ALL SELECT 'UNIDADE POPULAR', 'EXTREMA-ESQUERDA'
    UNION ALL SELECT 'UNIÃO BRASIL', 'CENTRO-DIREITA'
),

tb_final as (
    select t3.*, t4.IDEOLOGIA 
    from tb_completa as t3
    inner join partidos_ideologia as t4
    on t3.NM_PARTIDO = t4.NM_PARTIDO
),

genero_partido AS (
    SELECT
        NM_PARTIDO,
        AVG(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) *100 AS tx_feminino,
        AVG(CASE WHEN DS_GENERO = 'MASCULINO' THEN 1 ELSE 0 END) *100 AS tx_masculino
    FROM tb_final
    GROUP BY NM_PARTIDO
),

cor_por_partido as (
    select NM_PARTIDO, ideologia,
avg(case when DS_COR_RACA IN ('PRETA' , 'PARDA') THEN 1 ELSE 0 END) *100 as tx_pretos_pardos,
avg(case when DS_COR_RACA = 'BRANCA' THEN 1 ELSE 0 END) *100 as tx_brancos,
avg(case when DS_COR_RACA = 'AMARELA' THEN 1 ELSE 0 END) *100 as tx_amarelos,
avg(case when DS_COR_RACA = 'INDÍGENA' THEN 1 ELSE 0 END) *100 as tx_indigena,
avg(case when DS_COR_RACA in ( 'NÃO INFORMADO', 'NÃO DIVULGADO') THEN 100 ELSE 0 END) as tx_Nulos

from tb_final
GROUP by NM_PARTIDO
),

eleitos_partido as (
    select NM_PARTIDO, ideologia, COUNT(SQ_CANDIDATO) AS total_candidatos,
    sum(case when DS_SIT_TOT_TURNO = 'ELEITO' then 1 else 0 end) *100 as numero_eleitos,
    avg(case when DS_SIT_TOT_TURNO = 'ELEITO' then 1 else 0 end) *100 as porcentagem_eleitos
    from tb_final
    group by NM_PARTIDO
),

bens_por_partido as (
select NM_PARTIDO , sum(totalBens) as soma_de_bens
from tb_final
group by NM_PARTIDO
),

Prefeitos_por_turno as (SELECT
  NR_TURNO,
  COUNT(DISTINCT SQ_CANDIDATO) AS total_candidatos
FROM tb_final
WHERE DS_CARGO = 'PREFEITO'
GROUP BY NR_TURNO
),

escolaridade_por_partido as (
    select NM_PARTIDO, ideologia,
avg(case when DS_GRAU_INSTRUCAO in ('LÊ E ESCREVE','ENSINO FUNDAMENTAL INCOMPLETO', 'ENSINO MÉDIO INCOMPLETO', 'ANALFABETO', 'ENSINO FUNDAMENTAL COMPLETO') THEN 1 ELSE 0 END) *100 as tx_baixa_escolaridade,
avg(case when DS_GRAU_INSTRUCAO in ('SUPERIOR INCOMPLETO','ENSINO MÉDIO COMPLETO') THEN 1 ELSE 0 END) *100 as tx_escolarizados,
avg(case when DS_GRAU_INSTRUCAO = 'SUPERIOR COMPLETO' THEN 1 ELSE 0 END) *100 as tx_superior_completo
from tb_final
GROUP by NM_PARTIDO
),


eleitos_por_ideologia as (
    select ideologia, count(*) as candidatos_eleitos
    from tb_final
    where DS_SIT_TOT_TURNO = 'ELEITO'
    group by ideologia
),


total_eleitos AS (
    SELECT SUM(candidatos_eleitos) AS total_eleitos
    FROM eleitos_por_ideologia
),

porcentagem_eleito_ideologia as (
    select t.ideologia, t.candidatos_eleitos, 
    round((1.0 * candidatos_eleitos / e.total_eleitos) * 100,2) as percentual
    from eleitos_por_ideologia as t
    cross join total_eleitos as e 
),

raca_por_ideologia as (
    select t.ideologia, avg(e.tx_pretos_pardos) as media_tx_pretos_pardos, 
    avg(e.tx_brancos) as media_tx_brancos,
    avg(e.tx_amarelos) as media_tx_amarelos,
    avg(e.tx_indigena) as media_tx_indigenas
    from tb_final as t 
    inner join cor_por_partido as e on t.NM_PARTIDO = e.NM_PARTIDO 
    group by t.ideologia
),

genero_por_ideologia as (
    select t.ideologia, avg(e.tx_feminino) as media_mulheres,
    avg(e.tx_masculino) as media_homens
    from tb_final as t 
    inner join genero_partido as e on t.NM_PARTIDO = e.NM_PARTIDO     
    GROUP BY t.ideologia
),

escolaridade_por_ideologia as (
    select t.ideologia, avg(e.tx_baixa_escolaridade) as media_baixa_escolaridade,
    avg(e.tx_escolarizados) as media_escolarizados,
    avg(e.tx_superior_completo) as media_graduados
    from tb_final as t inner join escolaridade_por_partido as e 
    on t.NM_PARTIDO = e.NM_PARTIDO
    group by t.ideologia
),

bens_por_ideologia as (
    select t.ideologia, avg(e.soma_de_bens) as media_bens
    from tb_final as t inner join bens_por_partido as e 
    on t.NM_PARTIDO = e.NM_PARTIDO
    group by t.ideologia 
),

cassados_por_ideologia as (
select t.ideologia, count(e.SQ_CANDIDATO) as qtde_cassados 
from tb_final as t inner join tb_cassacao as e 
on t.SQ_CANDIDATO = e.SQ_CANDIDATO
group by t.ideologia
),


cassados_por_partido as (
select t.NM_PARTIDO, count(e.SQ_CANDIDATO) as qtde_cassados 
from tb_final as t inner join tb_cassacao as e 
on t.SQ_CANDIDATO = e.SQ_CANDIDATO
group by 1
),

tabela_resumo as (
SELECT
    p.ideologia,
    p.percentual AS pct_eleitos,
    g.media_mulheres,
    r.media_tx_pretos_pardos,
    e.media_graduados,
    b.media_bens,
    c.qtde_cassados
FROM porcentagem_eleito_ideologia p
LEFT JOIN genero_por_ideologia g ON p.ideologia = g.ideologia
LEFT JOIN raca_por_ideologia r ON p.ideologia = r.ideologia
LEFT JOIN escolaridade_por_ideologia e ON p.ideologia = e.ideologia
LEFT JOIN bens_por_ideologia b ON p.ideologia = b.ideologia
LEFT JOIN cassados_por_ideologia c ON p.ideologia = c.ideologia
),

tb_final2 as (
    select t3.*,
    CASE 
        WHEN t5.DS_MOTIVO IS NOT NULL THEN 'Sim'  
        ELSE  'Não'  
    END as Status_Cassacao
    from tb_final as t3
    left join tb_cassacao as t5 on t3.SQ_CANDIDATO = t5.SQ_CANDIDATO
)

select * from tb_final2