#!/usr/bin/env python3
import sys
import locale
import os
#Caso a importacao do modulo Dialog falhe, executa-se a instalacao do modulo
try:
	from dialog import Dialog
except ImportError:
	os.system("sudo apt install -y python3-dialog")

locale.setlocale(locale.LC_ALL, '')

#criando uma instancia Dialog
d = Dialog(dialog="dialog")
interfaces = []
interfaces=os.popen("ls /sys/class/net | grep -v lo").read().strip().split("\n")

def conf_manual():
	os.system("echo 'auto lo \n iface lo inet loopback' > /etc/network/interfaces")

	for i in interfaces:
		if d.yesno("Deseja habilitar a interface " + i + " com DHCP?") == d.OK:
			os.system("echo 'auto " + i + "\niface " + i + " inet dhcp' >> /etc/network/interfaces")
		else:
			code, ipaddr = d.inputbox("Digite o IP da interface " + i,"")
			code, netmask = d.inputbox("Digite a mascara de rede","")
			os.system("echo 'auto " + i + "\niface " + i + " inet static\naddress " + ipaddr + "\nnetmask " + netmask + "' >> /etc/network/interfaces")

	code, namesrv = d.inputbox("Digite o IP do servidor DNS","")
	os.system("echo 'nameserver " + namesrv + "' > /etc/resolv.conf")

	confs = os.popen("cat /etc/network/interfaces").read()
	d.msgbox(confs,0,0)

def arp():
	code, arp_params = d.inputbox("Digite os parametros do comando ARP a ser executado","")
	arp_output = os.popen("arp " + arp_params).read()
	d.msgbox(arp_output,0,0)

#TELA INICIAL
def tela_inicial():
	#Chamada da janela dialog
	code, tag = d.menu("Escolha a VM a ser configurada",choices=[("VM1",""),("VM2",""),("VM3",""),("VM4",""),("SAIR","")])
	return tag

#ROTINA DE CONFIGURACAO DA VM1
def vm1_conf():
	code, tag = d.menu("Tela de Controle da VM1",choices=[("AUTOIP","Configuracao Automatica"),("MANUAL","Configuracao Manual TCP/IP"),("CONF","Listar Configuracoes"),\
("ARP","Executar Comando ARP"),("VOLTAR","")])

	if tag == "AUTOIP":
		os.system("echo 'auto lo \n iface lo inet loopback\n\
auto " + interfaces[0] + "\n iface " + interfaces[0] + " inet static\n address 192.168.10.2\n netmask 255.255.255.0\n gateway 192.168.10.1' > /etc/network/interfaces")
		os.system("echo 'nameserver 8.8.8.8\nnameserver 8.8.4.4' > /etc/resolv.conf")

		#exibir configuracoes
		confs = os.popen("cat /etc/network/interfaces").read()
		d.msgbox(confs,0,0)

	elif tag == "MANUAL":
		conf_manual()
	elif tag == "CONF":
		confs = os.popen("cat /etc/network/interfaces").read()
		d.msgbox(confs,0,0)

	#EXECUCAO DO COMANDO ARP
	elif tag == "ARP":
		arp()

	else:
		return


##############################################################################################################################################################################
# CONFIGURACAO DA VM2 QUE ESTA PREVISTA COMO SENDO A VM CONECTADA A REDE NAT
# ATUANDO COMO ROTEADOR DE SAIDA PARA A INTERNET
###############################################################################################################################################################################
def vm2_conf():
	#chamada da janela dialog
	code, tag = d.menu("Tela de Controle da VM2",choices=[("AUTOIP","Configuracao Automatica"),("MANUAL","Configuracao Manual TCP/IP"),("CONF","Listar Configuracoes"),("VOLTAR","")])

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
		conf_manual()

	elif tag == "CONF":
		#exibindo a configuracao realizada
		confs_ifaces = os.popen("cat /etc/network/interfaces").read()
		confs_iptables = os.popen("iptables -L && iptables -t nat -L").read()
		d.msgbox("INTERFACES DE REDE\n" + confs_ifaces + "\nFIREWALL\n\n" + confs_iptables,40,70)

	else:
		#caso o usuario selecione a opcao "VOLTAR", "Cancelar" ou aperte a tecla ESC.
		#finaliza a execucao da funcao e volta para o loop infinito
		return
####################################################################################################################################################################

#ROTINA DE CONFIGURACAO DA VM3.

def vm3_conf():
	code, tag = d.menu("Tela de Controle da VM3",choices=[("AUTOIP","Configuracao Automatica"),("MANUAL","Configuracao Manual TCP/IP"),("CONF","Listar Configuracoes"),("VOLTAR","")])

	if tag == "AUTOIP":
		os.system("echo 'auto lo \n iface lo inet loopback\n\
auto " + interfaces[0] + "\n iface " + interfaces[0] + " inet static\n address 172.24.1.2\n netmask 255.255.255.0\n gateway 172.24.1.1\n\
auto " + interfaces[1] + "\n iface " + interfaces[1] + " inet static\n address 192.168.2.1\n netmask 255.255.255.0' > /etc/network/interfaces")
		os.system("echo 'nameserver 8.8.8.8\nnameserver 8.8.4.4' > /etc/resolv.conf")
		confs = os.popen("cat /etc/network/interfaces").read()
		d.msgbox(confs,0,0)

	elif tag == "MANUAL":
		conf_manual()
	elif tag == "CONF":
		confs = os.popen("cat /etc/network/interfaces").read()
		d.msgbox(confs,0,0)
	else:
		return

###############################################################################################################################################
#ROTINA DE CONFIGURACAO DA VM4.
#########################################

def vm4_conf():
	code, tag = d.menu("Tela de Controle da VM4",choices=[("AUTOIP","Configuracao Automatica"),("MANUAL","Configuracao Manual TCP/IP"),("CONF","Listar Configuracoes"),("VOLTAR","")])
	interfaces=[]
	interfaces=os.popen("ip link | awk '$0 ~ \"enp0s[0-9]\" {gsub(\":\",\"\"); print $2}'").read().strip().split("\n")

	if tag == "AUTOIP":
		os.system("echo 'auto lo \n iface lo inet loopback\n\
auto " + interfaces[0] + "\n iface " + interfaces[0] + " inet static\n address 192.168.2.2\n netmask 255.255.255.0\n gateway 192.168.2.1' > /etc/network/interfaces")
		os.system("echo 'nameserver 8.8.8.8\nnameserver 8.8.4.4' > /etc/resolv.conf")
		confs = os.popen("cat /etc/network/interfaces").read()
		d.msgbox(confs,0,0)

	elif tag == "MANUAL":
		conf_manual()
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
	elif opcao == "VM4":
		vm4_conf()
	else:
		#Caso o usuario selecione 'cancelar' ou pressione a tecla ESC.
		sys.exit(0)
