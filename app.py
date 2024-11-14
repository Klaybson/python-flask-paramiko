from flask import Flask, render_template, redirect, url_for, flash, session
import paramiko

app = Flask(__name__)
app.secret_key = 'vida'  # Substitua por uma chave secreta segura

def restart_remote_system():
    hostname = "192.168.1.31"
    username = "root"
    password = "SENHA"
    command = "systemctl restart apache2"

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(command)
        flash("Comando executado com sucesso!", 'success')
        return stdout.read().decode()
    except paramiko.AuthenticationException:
        flash("Erro de autenticação. Verifique suas credenciais.", 'danger')
    except paramiko.SSHException as e:
        flash(f"Erro de conexão SSH: {str(e)}", 'danger')
    except Exception as e:
        flash(f"Erro inesperado: {str(e)}", 'danger')
    finally:
        client.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/restart', methods=['POST'])
def restart():
    restart_remote_system()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
