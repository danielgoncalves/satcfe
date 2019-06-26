# -*- coding: utf-8 -*-
#
# satcfe/tests/test_desbloquearsat.py
#
# Copyright 2019 Base4 Sistemas Ltda ME
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import pytest

from unidecode import unidecode

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaSAT


def test_respostas_de_sucesso(datadir):
    with open(datadir.join('respostas-de-sucesso.txt'), 'r') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        resposta = RespostaSAT.desbloquear_sat(retorno)
        assert resposta.EEEEE == '17000'  # único código de sucesso possível


def test_respostas_de_falha(datadir):
    with open(datadir.join('respostas-de-falha.txt'), 'r') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ExcecaoRespostaSAT):
            RespostaSAT.desbloquear_sat(retorno)


def test_respostas_invalidas(datadir):
    with open(datadir.join('respostas-invalidas.txt'), 'r') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ErroRespostaSATInvalida):
            RespostaSAT.desbloquear_sat(retorno)


@pytest.mark.acessa_sat
@pytest.mark.invoca_desbloquearsat
def test_desbloquearsat(request, clientesatlocal):
    # Este teste baseia-se na resposta da biblioteca SAT de simulação (mockup)
    # que é usada nos testes do projeto SATHub:
    # https://github.com/base4sistemas/sathub
    #
    resposta = clientesatlocal.desbloquear_sat()
    assert resposta.EEEEE == '17000'
    assert unidecode(resposta.mensagem).lower() == (
            'equipamento sat desbloqueado com sucesso'
        )
