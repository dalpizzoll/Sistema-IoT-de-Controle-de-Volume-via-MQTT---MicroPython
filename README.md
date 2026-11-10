# 🌊 Sistema IoT de Monitoramento e Controle de Volume via MQTT (MicroPython)

Este projeto implementa um sistema de automação e telemetria embarcado em **MicroPython** para controle e monitoramento em tempo real de um processo de reservatório/tanque. O sistema se comunica com a plataforma **ThingsBoard** utilizando o protocolo **MQTT**, permitindo a leitura de telemetria contínua e a execução de comandos remotos (RPC).

---

## 📌 Funcionalidades

- **📡 Telemetria em Tempo Real:** Envio periódico (a cada 500 ms) dos valores de volume e vazão com *timestamp* no formato POSIX/Unix.
- **🕹️ Comandos Remotos (RPC):** Aceita requisições HTTP/MQTT do ThingsBoard para acionamento de atuadores (bomba e válvula de saída) e parametrização de setpoints (vazão e volume).
- **⏰ Sincronização Temporal (NTP):** Ajuste do relógio do microcontrolador via servidor NTP para carimbo de data/hora preciso.
- **🔄 Conectividade e Resiliência:** Conexão automática via Wi-Fi com reinicialização automática (`reset()`) em caso de falha de conexão.

---

## 🛠️ Arquitetura e Tópicos MQTT

O código segue a especificação da API MQTT do **ThingsBoard**:

| Canal / Recurso | Tópico MQTT | Descrição |
| :--- | :--- | :--- |
| **Telemetria** | `v1/devices/me/telemetry` | Publicação de volume e vazão em formato JSON. |
| **Requisição RPC** | `v1/devices/me/rpc/request/+` | Inscrição para recepção de comandos do servidor. |
| **Resposta RPC** | `v1/devices/me/rpc/response/{id}` | Resposta com o estado atual do parâmetro solicitado. |

---

## 📋 Métodos RPC Suportados

| Método | Tipo | Parâmetros (`params`) | Descrição |
| :--- | :--- | :--- | :--- |
| `setSaida` | Escrita | `bool` (`true`/`false`) | Liga ou desliga a válvula de saída. |
| `getSaida` | Leitura | — | Retorna o status atual da válvula de saída. |
| `setBomba` | Escrita | `bool` (`true`/`false`) | Liga ou desliga a bomba de enchimento. |
| `getBomba` | Leitura | — | Retorna o status atual da bomba. |
| `setVazao` | Escrita | `int` / `float` | Define o valor de vazão do sistema. |
| `getVazao` | Leitura | — | Retorna o valor de vazão atual. |
| `setVolume` | Escrita | `int` / `float` | Define o nível de volume do tanque. |
| `getVolume` | Leitura | — | Retorna o nível de volume atual. |

---

## 📁 Estrutura de Arquivos Necessária

Para o funcionamento correto do código, o sistema de arquivos do dispositivo MicroPython deve possuir a seguinte estrutura:

```text
├── main.py          # Código principal do cliente MQTT e RPC
├── config.json      # Arquivo de configuração de rede e broker
├── rede.py          # Módulo auxiliar para gerenciamento da conexão Wi-Fi
└── processo.py      # Classe 'Volume' com a lógica/simulação física do tanque
```

### Exemplo de `config.json`
```json
{
  "rede": "Sua_Rede_WiFi",
  "senha": "Sua_Senha_WiFi",
  "broker": "iot.thingsboard.cloud",
  "clientId": "ESP32_Volume_Control",
  "userbroker": "SEU_ACCESS_TOKEN_THINGSBOARD"
}
```

---

## 🚀 Como Executar

1. **Upload dos Arquivos:** Carregue os arquivos `main.py`, `config.json`, `rede.py` e `processo.py` para a memória do microcontrolador (ESP32/ESP8266) usando ferramentas como **Thonny IDE**, **ampy** ou **VS Code (Pymakr)**.
2. **Dependências:** Certifique-se de que as bibliotecas `umqtt.robust` e `ntptime` estejam instaladas ou disponíveis na firmware do MicroPython.
3. **Execução:**
   - Preencha o `config.json` com suas credenciais de Wi-Fi e o *Access Token* do dispositivo ThingsBoard.
   - Execute o arquivo `main.py` (ou reinicie o microcontrolador).

---

## 📊 Exemplo do Payload de Telemetria (JSON)

```json
{
  "ts": 1773238020000,
  "values": {
    "volume": 250.5,
    "vazao": 12.0
  }
}
```
