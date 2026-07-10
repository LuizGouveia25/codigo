# Instruções de Deployment e Manutenção - Autenticador TOTP

Este documento contém as instruções necessárias para implantar, configurar e manter o Autenticador TOTP da Equipe Jurídica.

## 1. Visão Geral

O Autenticador TOTP é uma aplicação web de página única (Single Page Application - SPA) contida inteiramente no arquivo `autenticador-totp.html`. Ele não requer backend ou banco de dados complexo, utilizando o armazenamento local do navegador para auditoria e controle de tentativas de login.

A segurança é garantida através de:
- Hashes bcrypt para senhas (armazenadas no próprio código).
- Geração de TOTP em tempo real usando a Web Crypto API nativa do navegador.
- Ausência de dependências externas para a lógica criptográfica principal (apenas bibliotecas visuais via CDN).

## 2. Deployment

Como a aplicação é um arquivo HTML estático, o deployment é extremamente simples e pode ser feito em qualquer servidor web (Nginx, Apache, IIS) ou serviço de hospedagem estática (GitHub Pages, Vercel, Netlify, AWS S3).

### 2.1. Requisito Obrigatório: HTTPS
A Web Crypto API (necessária para gerar o TOTP) **só funciona em contextos seguros (HTTPS)**. Se você tentar acessar a página via HTTP (exceto em `localhost`), o gerador TOTP falhará.

**Passos para Servidor Web Tradicional (ex: Nginx):**
1. Copie o arquivo `autenticador-totp.html` para o diretório raiz do seu servidor web (ex: `/var/www/html/`).
2. Renomeie o arquivo para `index.html` (opcional, para acesso direto via URL base).
3. Configure o servidor para forçar o redirecionamento de HTTP para HTTPS.
4. Instale um certificado SSL/TLS (recomenda-se Let's Encrypt / Certbot).

Exemplo de configuração Nginx:
```nginx
server {
    listen 80;
    server_name totp.seudominio.com.br;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name totp.seudominio.com.br;

    ssl_certificate /etc/letsencrypt/live/totp.seudominio.com.br/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/totp.seudominio.com.br/privkey.pem;

    root /var/www/html;
    index autenticador-totp.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

## 3. Configuração e Manutenção

Todas as configurações são feitas diretamente no arquivo `autenticador-totp.html`, na seção `CONFIGURAÇÕES E DADOS SENSÍVEIS` (linha 166).

### 3.1. Inserindo a Chave TOTP do TJMG

1. Abra o arquivo `autenticador-totp.html` em um editor de texto.
2. Localize a constante `TOTP_SECRET`.
3. Substitua o valor `"JBSWY3DPEHPK3PXP"` pela chave Base32 fornecida pelo TJMG.
   ```javascript
   const TOTP_SECRET = "SUA_CHAVE_BASE32_AQUI";
   ```
   *Nota: A chave deve conter apenas caracteres válidos do alfabeto Base32 (A-Z, 2-7).*

### 3.2. Gerenciamento de Usuários e Senhas

As senhas não são armazenadas em texto puro, mas sim em hashes gerados pelo algoritmo **bcrypt**.

**Para adicionar um novo usuário ou alterar uma senha:**

1. Você precisa gerar um hash bcrypt (fator de custo 12 recomendado).
2. Você pode gerar o hash usando Python, Node.js ou ferramentas online seguras.

**Exemplo usando Python:**
```python
import bcrypt
senha = b"nova_senha_secreta"
hash_gerado = bcrypt.hashpw(senha, bcrypt.gensalt(rounds=12))
print(hash_gerado.decode())
# Saída esperada: $2b$12$...
```

**Exemplo usando Node.js:**
```javascript
const bcrypt = require('bcryptjs');
const hashGerado = bcrypt.hashSync("nova_senha_secreta", 12);
console.log(hashGerado);
```

3. No arquivo `autenticador-totp.html`, localize a constante `USERS`.
4. Adicione, edite ou remova entradas do objeto:
   ```javascript
   const USERS = {
       "colaborador1": "$2b$12$DK0lSXjEo9IODlR7MG1aUO/GRiG9z5O/XbzYPbm4ReVwMYm6MTua2", // senha123
       "colaborador2": "$2b$12$lMwkR24NXUhrNQfVELYBaOMXYQRZRXhC7D1aHCdmfTzs.FtrLlqfC", // senha456
       "colaborador3": "$2b$12$DEQBwJ25uGJ0/orXc0Vu/O.eVLKcMdkvFxchzIuS6PYrXSK4aa.bi", // senha789
       "novo_usuario": "$2b$12$SeuNovoHashGeradoAqui..."
   };
   ```

## 4. Auditoria e Logs

A aplicação registra eventos importantes (logins com sucesso, falhas, bloqueios, códigos copiados) no `localStorage` do navegador do usuário.

- **Exportação:** Qualquer usuário logado pode clicar em "Exportar Logs" no rodapé da aplicação para baixar um arquivo CSV com os últimos 100 eventos registrados naquele navegador específico.
- **Privacidade:** Os logs são mantidos apenas no navegador local (client-side) e não são enviados para nenhum servidor.
- **Limpeza:** Limpar os dados de navegação (cache/localStorage) do navegador apagará o histórico de auditoria.

## 5. Segurança

- **Rate Limiting:** A aplicação bloqueia o usuário por 5 minutos após 5 tentativas de login incorretas.
- **Sessão:** A sessão expira automaticamente após 30 minutos de inatividade, exigindo novo login.
- **Armazenamento:** A chave TOTP nunca é salva no `localStorage` ou `sessionStorage`, existindo apenas na memória durante a execução.
