# Switch Automation

Automação das configurações de switches usando o Netbox como elemento de orquestração.

LEIA o PDF contendo as informações necessarias para o entendimento do projeto.

## Instalação Netbox

Seguir: [Getting Started](https://github.com/netbox-community/netbox-docker/wiki/Getting-Started)

### Com o Netbox UP, entrar nos menus

- **Device Types**: Criar os modelos de switches (Criar interfaces padrões dos dispositivos).
- **Device**: Criar um switch de acordo com um modelo criado anteriormente.
- **IPAM**: Criar range de ips internos.
- **Interfaces**: Criar interfaces extras como interfaces virtuais e associar o ip do switch.
- **Webhook**: Criar webhook para chamada do webservice sempre que ocorrer uma atulização nas interfaces (dcim/interfaces), colocar <IP:PORTA> do webservice

## Webservice

Roda o webservice em container

A imagem será criada a partir do Dockerfile e usada pelo docker-compose


```bash
docker-compose up -d
```


Com isso uma vez que alguma interface for editada o webhook do Netbox irá chamar o webservice que se encarregara de filtrar as informações e aplicar no dispositivo fisico que foi atualizado na documentação.
