import smtplib, poplib, imaplib, ssl, socket, time, os, platform

TIMEOUT = 6

# --- Detecção do sistema para limpar tela ---
def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")

# --- Funções de teste ---
def timed_test(func, *args):
    inicio = time.perf_counter()
    result = func(*args)
    fim = time.perf_counter()
    duracao = (fim - inicio) * 1000
    return result, round(duracao, 2)

def test_socket(host, port):
    try:
        with socket.create_connection((host, port), timeout=TIMEOUT):
            return "OK"
    except Exception as e:
        return f"Erro"

def test_smtp_ssl(host, port=465):
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=context, timeout=TIMEOUT) as s:
            s.noop()
        return "OK"
    except Exception:
        return "Erro"

def test_smtp_tls(host, port=587):
    try:
        with smtplib.SMTP(host, port, timeout=TIMEOUT) as s:
            s.starttls()
            s.noop()
        return "OK"
    except Exception:
        return "Erro"

def test_pop_ssl(host, port=995):
    try:
        with poplib.POP3_SSL(host, port, timeout=TIMEOUT) as p:
            p.getwelcome()
        return "OK"
    except Exception:
        return "Erro"

def test_pop_plain(host, port=110):
    try:
        with poplib.POP3(host, port, timeout=TIMEOUT) as p:
            p.getwelcome()
        return "OK"
    except Exception:
        return "Erro"

def test_imap_ssl(host, port=993):
    try:
        context = ssl.create_default_context()
        with imaplib.IMAP4_SSL(host, port, ssl_context=context) as i:
            i.noop()
        return "OK"
    except Exception:
        return "Erro"

def test_imap_plain(host, port=143):
    try:
        with imaplib.IMAP4(host, port, timeout=TIMEOUT) as i:
            i.noop()
        return "OK"
    except Exception:
        return "Erro"


# --- Modo 1: Teste rápido ---
def modo_teste_rapido(server):
    print("\n=== TESTE RÁPIDO DE CONEXÕES ===")
    print(f"Servidor: {server}\n")

    tests = [
        ("SMTP 25 (plain)", test_socket, server, 25),
        ("SMTP 465 (SSL)", test_smtp_ssl, server),
        ("SMTP 587 (TLS)", test_smtp_tls, server),
        ("POP3 110 (plain)", test_pop_plain, server),
        ("POP3 995 (SSL)", test_pop_ssl, server),
        ("IMAP 143 (plain)", test_imap_plain, server),
        ("IMAP 993 (SSL)", test_imap_ssl, server)
    ]

    for nome, func, *args in tests:
        status, ms = timed_test(func, *args)
        print(f"{nome:<20}: {status:<10} ({ms} ms)")

    print("\n--- Teste concluído ---\n")


# --- Modo 2: Painel em tempo real ---
def modo_tempo_real(server):
    print("\n=== VISUALIZAÇÃO EM TEMPO REAL ===")
    print("Pressione Ctrl+C para sair.\n")

    tests = [
        ("SMTP 25", test_socket, server, 25),
        ("SMTP 465", test_smtp_ssl, server),
        ("SMTP 587", test_smtp_tls, server),
        ("POP3 110", test_pop_plain, server),
        ("POP3 995", test_pop_ssl, server),
        ("IMAP 143", test_imap_plain, server),
        ("IMAP 993", test_imap_ssl, server)
    ]

    try:
        while True:
            resultados = []
            for nome, func, *args in tests:
                status, ms = timed_test(func, *args)
                resultados.append((nome, status, ms))

            clear()
            print(f"=== MONITOR TEMPO REAL ({server}) === {time.strftime('%H:%M:%S')}\n")

            for nome, status, ms in resultados:
                cor_status = "\033[92m" if status == "OK" else "\033[91m"
                cor_reset = "\033[0m"
                print(f"{nome:<12} | {cor_status}{status:<5}{cor_reset} | {ms:>7} ms")

            print("\nAtualizando a cada 2s... (Ctrl+C para sair)")
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n\nMonitoramento encerrado.\n")


# --- Execução principal ---
print("=== MONITOR DE E-MAIL ===")
server = input("Digite o domínio ou IP do servidor: ").strip()

print("""
Escolha o modo:
1 - Teste Rápido
2 - Visualização em Tempo Real
""")

opcao = input("Opção: ").strip()

if opcao == "1":
    modo_teste_rapido(server)
elif opcao == "2":
    modo_tempo_real(server)
else:
    print("Opção inválida. Saindo...")
