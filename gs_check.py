import os
import pwd
import argparse


def set_folder(folder, user, chmod):
    os.makedirs(folder, exist_ok=True)

    # Get UID user
    uid_user = pwd.getpwnam(user).pw_uid

    # Perm
    os.chown(folder, uid_user, -1)
    os.chmod(folder, chmod)

    print('\n', 'Pasta criada com permissão para: {}'.format(user), '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Criar pasta com permissão")
    parser.add_argument("folder", type=str, help="Caminho da pasta a ser criada")
    parser.add_argument("user", type=str, help="Nome do usuário")
    parser.add_argument("chmod", type=int, help="Permissões (octal)")
    args = parser.parse_args()

    # Execute
    set_folder(args.folder, args.user, args.chmod)

# How to use
# python gs_check.py /tmp/saltstack/salt_softs svc.jenkins.local 755
