#!/usr/bin/env python3
import sys
import locale
import os
#Caso a importacao do modulo Dialog falhe, executa-se a instalacao do modulo
try:
	from dialog import Dialog
except ImportError:
	os.system("sudo apt install python3-dialog")

locale.setlocale(locale.LC_ALL, '')

#criando uma instancia Dialog
d = Dialog(dialog="dialog")

#TELA INICIAL
def tela_inicial():
	#Chamada da janela dialog
	code, tag = d.menu("Escolha a VM a ser configurada",choices=[("VM1",""),("VM2",""),("VM3",""),("SAIR","")])
	return tag

#ROTINA DE CONFIGURACAO DA VM1
def vm1_conf():
	#chamada da janela dialog
	code, tag = d.menu("Tela de Controle da VM1",choices=[("AUTOIP","Configuracao Automatica"),("MANUAL","Configuracao Manual TCP/IP"),("CONF","Listar Configuracoes"),("VOLTAR","")])
	interfaces=[]
	#obentdo a lista de interfaces de rede da VM e salvando em interfaces[]
	#filtrando a saida do comando "ip link", com o AWK, buscndo ocorrencias de strings iniciando em 'enp0s' seguidas por um numero de 0 a 9.
	interfaces=os.popen("ip link | awk '$0 ~ \"enp0s[0-9]\" {gsub(\":\",\"\"); print $2}'").read().strip().split("\n")

#Sequencia de IFs verificando o conteudo da variavel TAG obtida como resposta do dialog de menu executado anteriormente.
	if tag == "AUTOIP":
		os.system("echo 'auto lo \n iface lo inet loopback\n\
auto " + interfaces[0] + "\n iface " + interfaces[0] + " inet dhcp\n\
auto " + interfaces[1] + "\n iface " + interfaces[1] + " inet static\n address 192.168.10.1\n netmask 255.255.255.0\n\
auto " + interfaces[2] + "\n iface " + interfaces[2] + " inet static\n address 172.24.1.1\n netmask 255.255.255.0' > /etc/network/interfaces")
		#Configuracao do iptables
		os.system("iptables -t nat -F")
		os.system("iptables -t nat -A POSTROUTING -o " + interfaces[0] + " -j MASQUERADE")

		#exibindo a configuracao realizada
		confs_ifaces = os.popen("cat /etc/network/interfaces").read()
		confs_iptables = os.popen("iptables -L && iptables -t nat -L").read()
		d.msgbox("INTERFACES DE REDE\n" + confs_ifaces + "\nFIREWALL\n\n" + confs_iptables,40,70)

	elif tag == "MANUAL":
		code, ipaddr1 = d.inputbox("Digite o IP da interface Eth1","")
		code, netmask1 = d.inputbox("Digite a mascara de rede","")
		code, ipaddr2 = d.inputbox("Digite o IP da interface Eth2","")
		code, netmask2 = d.inputbox("Digite a mascara de rede","")
		os.system("echo 'auto lo \n iface lo inet loopback\n\
auto " + interfaces[0] + "\n iface " + interfaces[0] + " inet dhcp\n\
auto " + interfaces[1] + "\n iface " + interfaces[1] + " inet static\n address " + ipaddr1 + "\n netmask " + netmask1 + "\n\
auto " + interfaces[2] + "\n iface " + interfaces[2] + " inet static\n address " + ipaddr2 + "\n netmask " + netmask2 + "' > /etc/network/interfaces")
	elif tag == "CONF":
		#exibindo a configuracao realizada
		confs_ifaces = os.popen("cat /etc/network/interfaces").read()
		confs_iptables = os.popen("iptables -L && iptables -t nat -L").read()
		d.msgbox("INTERFACES DE REDE\n" + confs_ifaces + "\nFIREWALL\n\n" + confs_iptables,40,70)

	else:
		#caso o usuario selecione a opcao "VOLTAR", "Cancelar" ou aperte a tecla ESC.
		#finaliza a execucao da funcao e volta para o loop infinito
		return

#ROTINA DE CONFIGURACAO DA VM2, seguindo o mesmo padrao da vm1, com a variacao do numero de interfaces configuradas.
def vm2_conf():
	code, tag = d.menu("Tela de Controle da VM2",choices=[("AUTOIP","Configuracao Automatica"),("MANUAL","Configuracao Manual TCP/IP"),("CONF","Listar Configuracoes"),("VOLTAR","")])
	interfaces=[]
	interfaces=os.popen("ip link | awk '$0 ~ \"enp0s[0-9]\" {gsub(\":\",\"\"); print $2}'").read().strip().split("\n")

	if tag == "AUTOIP":
		os.system("echo 'auto lo \n iface lo inet loopback\n\
auto " + interfaces[0] + "\n iface " + interfaces[0] + " inet static\n address 192.168.10.2\n netmask 255.255.255.0\n gateway 192.168.10.1' > /etc/network/interfaces")
		os.system("echo 'nameserver 8.8.8.8\nnameserver 8.8.4.4' > /etc/resolv.conf")
		confs = os.popen("cat /etc/network/interfaces").read()
		d.msgbox(confs,0,0)

	elif tag == "MANUAL":
		code, ipaddr1 = d.inputbox("Digite o IP da interface","")
		code, netmask1 = d.inputbox("Digite a mascara de rede","")
		code, gw1 = d.inputbox("Digite o IP do gateway","")
		code, namesrv = d.inputbox("Digite o IP do servidor DNS","")
		os.system("echo 'auto lo \n iface lo inet loopback\n\
auto " + interfaces[0] + "\n iface " + interfaces[0] + " inet static\n address " + ipaddr1 + "\n netmask " + netmask1 + "\n gateway " + gw1 + "' > /etc/network/interfaces")
		os.system("echo 'nameserver " + namesrv + "' > /etc/resolv.conf")

	elif tag == "CONF":
		confs = os.popen("cat /etc/network/interfaces").read()
		d.msgbox(confs,0,0)
	else:
		return

#ROTINA DE CONFIGURACAO DA VM2, seguindo o mesmo padrao da vm1, com a variacao do numero de interfaces configuradas.
def vm3_conf():
	code, tag = d.menu("Tela de Controle da VM3",choices=[("AUTOIP","Configuracao Automatica"),("MANUAL","Configuracao Manual TCP/IP"),("CONF","Listar Configuracoes"),("VOLTAR","")])
	interfaces=[]
	interfaces=os.popen("ip link | awk '$0 ~ \"enp0s[0-9]\" {gsub(\":\",\"\"); print $2}'").read().strip().split("\n")

	if tag == "AUTOIP":
		os.system("echo 'auto lo \n iface lo inet loopback\n\
auto " + interfaces[0] + "\n iface " + interfaces[0] + " inet static\n address 172.24.1.2\n netmask 255.255.255.0\n gateway 172.24.1.1' > /etc/network/interfaces")
		os.system("echo 'nameserver 8.8.8.8\nnameserver 8.8.4.4' > /etc/resolv.conf")
		confs = os.popen("cat /etc/network/interfaces").read()
		d.msgbox(confs,0,0)

	elif tag == "MANUAL":
		code, ipaddr1 = d.inputbox("Digite o IP da interface","")
		code, netmask1 = d.inputbox("Digite a mascara de rede","")
		code, gw1 = d.inputbox("Digite o IP do gateway","")
		code, namesrv = d.inputbox("Digite o IP do servidor DNS","")
		os.system("echo 'auto lo \n iface lo inet loopback\n\
auto " + interfaces[0] + "\n iface " + interfaces[0] + " inet static\n address " + ipaddr1 + "\n netmask " + netmask1 + "\n gateway " + gw1 + "' > /etc/network/interfaces")
		os.system("echo 'nameserver " + namesrv + "' > /etc/resolv.conf")

	elif tag == "CONF":
		confs = os.popen("cat /etc/network/interfaces").read()
		d.msgbox(confs,0,0)
	else:
		return

#LOOP infinito voltando a execucao da tela inicial
while True:
	opcao = tela_inicial()
	if opcao == "VM1":
		vm1_conf()
	elif opcao == "VM2":
		vm2_conf()
	elif opcao == "VM3":
		vm3_conf()
	else:
		#Caso o usuario selecione 'cancelar' ou pressione a tecla ESC.
		sys.exit(0)

