# Comando para compilar:
# pyinstaller --onefile --add-binary "msedgedriver.exe;." prueba.py
import sys
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchFrameException, ElementNotInteractableException
import time
import tempfile

from datetime import datetime

def verificar_fecha():
    try:
        # Obtener la fecha y hora actual del sistema
        fecha_actual = datetime.now()

        # Definir la fecha límite (1 de abril de 2025)
        fecha_limite = datetime(2025, 4, 1)

        # Comparar las fechas
        if fecha_actual < fecha_limite:
            print("La fecha del sistema es válida. Continuando con la ejecución del script.")
            return True
        else:
            print("La fecha del sistema supera la fecha límite. El script no se ejecutará.")
            return False
    except Exception as e:
        print(f"No se pudo obtener la fecha del sistema: {e}")
        return False

# Uso de la función en tu script de Selenium
if verificar_fecha():
    # Coloca aquí el código de tu script de Selenium
    pass
else:
    print("Finalizando la ejecución del script debido a la verificación de fecha fallida.")


# Determinar la ruta base
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

# Solicitar al usuario el nombre de red y la contraseña
user_ssid = input("Ingrese el nombre de la red WiFi (para el campo SSID): ")
wpa_pass = input("Ingrese la contraseña WPA/WAPI: ")

# Obtiene la ruta del driver en base a la ruta determinada
driver_path = os.path.join(base_path, "msedgedriver.exe")
service = Service(driver_path)
options = webdriver.EdgeOptions()
driver = webdriver.Edge(service=service, options=options)

try:
    print("Abriendo la página del módem...")
    driver.get("http://support:support@192.168.0.1")

    # Esperar a que el frame "menufrm" esté presente
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "menufrm"))
        )
        driver.switch_to.frame("menufrm")
        print("✅ Cambio al frame 'menufrm' exitoso.")
    except TimeoutException:
        print("❌ Error: No se encontró el frame 'menufrm'.")
        driver.quit()
        exit()

    # Buscar y hacer clic en "Advanced Setup"
    try:
        advanced_setup_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Advanced Setup')]"))
        )
        print("✅ Botón 'Advanced Setup' encontrado. Haciendo clic...")
        advanced_setup_button.click()
    except TimeoutException:
        print("❌ No se encontró el botón 'Advanced Setup'.")
        driver.quit()
        exit()
    
    driver.switch_to.default_content()  # Volver al contenido principal
    print("✅ Navegación a 'Advanced Setup' exitosa.")
    
    # Cambiar al frame que contiene el botón "Add"
    try:
        driver.switch_to.frame("basefrm")
        print("✅ Cambio al frame 'basefrm' exitoso.")
    except NoSuchElementException:
        print("❌ Error: No se encontró el frame 'basefrm'.")
        driver.quit()
        exit()

    # Esperar a que el botón "Add" esté presente y visible
    try:
        add_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Add']"))
        )
        print("✅ Botón 'Add' encontrado. Haciendo clic...")
        add_button.click()
    except TimeoutException:
        print("❌ No se encontró el botón 'Add' después de 10 segundos.")
        driver.quit()
        exit()

    # Esperar a que el botón "Apply/Save" esté presente y visible
    try:
        apply_save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Apply/Save']"))
        )
        print("✅ Botón 'Apply/Save' encontrado. Haciendo clic...")
        apply_save_button.click()
    except TimeoutException:
        print("❌ No se encontró el botón 'Apply/Save' después de 10 segundos.")
        driver.quit()
        exit()

    # Cambiar al frame que contiene el menú
    try:
        driver.switch_to.default_content()  # Volver al contenido principal
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "menufrm"))
        )
        driver.switch_to.frame("menufrm")
        print("✅ Cambio al frame 'menufrm' exitoso nuevamente.")
    except TimeoutException:
        print("❌ Error: No se encontró el frame 'menufrm'.")
        driver.quit()
        exit()

    # Buscar y hacer clic en "WAN Service"
    try:
        wan_service_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='menuLink' and @href='wancfg.cmd']"))
        )
        print("✅ Botón 'WAN Service' encontrado. Haciendo clic...")
        wan_service_button.click()
    except TimeoutException:
        print("❌ No se encontró el botón 'WAN Service'.")
        driver.quit()
        exit()
    
    driver.switch_to.default_content()  # Volver al contenido principal
    print("✅ Navegación a 'WAN Service' exitosa.")

    # Cambiar al frame que contiene el botón "Add" en WAN Service
    try:
        driver.switch_to.frame("basefrm")
        print("✅ Cambio al frame 'basefrm' exitoso para WAN Service.")
    except NoSuchFrameException:
        print("❌ Error: No se encontró el frame 'basefrm' después de WAN Service.")
        driver.quit()
        exit()

    # Esperar a que el botón "Add" esté presente y visible en WAN Service
    try:
        add_button_wan = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Add']"))
        )
        print("✅ Botón 'Add' en WAN Service encontrado. Haciendo clic...")
        add_button_wan.click()
    except TimeoutException:
        print("❌ No se encontró el botón 'Add' en WAN Service después de 10 segundos.")
        driver.quit()
        exit()

    # Esperar a que la opción "IP over Ethernet" esté presente y visible
    try:
        ip_over_ethernet_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='radio' and @name='ntwkPrtcl' and @onclick='prtclClick()'][following-sibling::text()[contains(., 'IP over Ethernet')]]"))
        )
        print("✅ Opción 'IP over Ethernet' encontrada. Haciendo clic...")
        ip_over_ethernet_option.click()
    except TimeoutException:
        print("❌ No se encontró la opción 'IP over Ethernet' después de 10 segundos.")
        driver.quit()
        exit()

    # Ingresar el número 5 en el campo "Enter 802.1P Priority [0-7]"
    try:
        priority_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @name='vlanMuxPr']"))
        )
        print("✅ Campo 'Enter 802.1P Priority [0-7]' encontrado. Ingresando valor 5...")
        priority_field.clear()
        priority_field.send_keys("5")
    except TimeoutException:
        print("❌ No se encontró el campo 'Enter 802.1P Priority [0-7]' después de 10 segundos.")
        driver.quit()
        exit()

    # Ingresar el número 500 en el campo "Enter 802.1Q VLAN ID [0-4094]"
    try:
        vlan_id_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @name='vlanMuxId']"))
        )
        print("✅ Campo 'Enter 802.1Q VLAN ID [0-4094]' encontrado. Ingresando valor 500...")
        vlan_id_field.clear()
        vlan_id_field.send_keys("500")
    except TimeoutException:
        print("❌ No se encontró el campo 'Enter 802.1Q VLAN ID [0-4094]' después de 10 segundos.")
        driver.quit()
        exit()

    # Hacer clic en el botón "Next"
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Next']"))
        )
        print("✅ Botón 'Next' encontrado. Haciendo clic...")
        next_button.click()
        print("✅ Se hizo clic en el botón 'Next'.")
    except TimeoutException:
        print("❌ No se encontró el botón 'Next' después de 10 segundos.")
        driver.quit()
        exit()
    time.sleep(5)

    # Hacer clic en el botón "Next" en la página "WAN IP Settings"
    try:
        next_button_wan_ip = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Next']"))
        )
        print("✅ Botón 'Next' en 'WAN IP Settings' encontrado. Haciendo clic...")
        next_button_wan_ip.click()
        print("✅ Se hizo clic en el botón 'Next' en 'WAN IP Settings'.")
    except TimeoutException:
        print("❌ No se encontró el botón 'Next' en 'WAN IP Settings' después de 10 segundos.")
        driver.quit()
        exit()

    # Seleccionar la casilla "Enable NAT"
    try:
        enable_nat_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and @name='enblNat' and @onclick='natClick(this)']"))
        )
        print("✅ Casilla 'Enable NAT' encontrada. Seleccionando...")
        enable_nat_checkbox.click()
    except TimeoutException:
        print("❌ No se encontró la casilla 'Enable NAT' después de 10 segundos.")
        driver.quit()
        exit()

    # Hacer clic en el botón "Next" en la página "Network Address Translation Settings"
    try:
        next_button_nat = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Next']"))
        )
        print("✅ Botón 'Next' en 'Network Address Translation Settings' encontrado. Haciendo clic...")
        next_button_nat.click()
        print("✅ Se hizo clic en el botón 'Next' en 'Network Address Translation Settings'.")
    except TimeoutException:
        print("❌ No se encontró el botón 'Next' en 'Network Address Translation Settings' después de 10 segundos.")
        driver.quit()
        exit()
    time.sleep(5)

    # Hacer clic en el botón "Next" en la página "Routing -- Default Gateway"
    try:
        next_button_routing = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Next']"))
        )
        print("✅ Botón 'Next' en 'Routing -- Default Gateway' encontrado. Haciendo clic...")
        next_button_routing.click()
        print("✅ Se hizo clic en el botón 'Next' en 'Routing -- Default Gateway'.")
    except TimeoutException:
        print("❌ No se encontró el botón 'Next' en 'Routing -- Default Gateway' después de 10 segundos.")
        driver.quit()
        exit()
    time.sleep(5)

    # Hacer clic en el botón "Next" en la página "DNS Server Configuration"
    try:
        next_button_dns = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Next']"))
        )
        print("✅ Botón 'Next' en 'DNS Server Configuration' encontrado. Haciendo clic...")
        next_button_dns.click()
        print("✅ Se hizo clic en el botón 'Next' en 'DNS Server Configuration'.")
    except TimeoutException:
        print("❌ No se encontró el botón 'Next' en 'DNS Server Configuration' después de 10 segundos.")
        driver.quit()
        exit()
    time.sleep(5)

    # Hacer clic en el botón "Apply/Save" en la página "WAN Setup - Summary"
    try:
        apply_save_button_summary = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @name='btnSave' and @value='Apply/Save']"))
        )
        print("✅ Botón 'Apply/Save' en 'WAN Setup - Summary' encontrado. Haciendo clic...")
        apply_save_button_summary.click()
        print("✅ Se hizo clic en el botón 'Apply/Save' en 'WAN Setup - Summary'.")
    except TimeoutException:
        print("❌ No se encontró el botón 'Apply/Save' en 'WAN Setup - Summary' después de 10 segundos.")
        driver.quit()
        exit()
    time.sleep(5)

    # RECONEXIÓN A LA RED WIFI
    # Se utiliza siempre "WiFi_network" para reconectar, sin importar lo ingresado por el usuario
    wifi_reconnect = "WiFi_network"
    print(f"🔄 Intentando reconectar a la red WiFi '{wifi_reconnect}'...")

    try:
        result = subprocess.run(
            ["netsh", "wlan", "connect", f"name={wifi_reconnect}"],
            capture_output=True, text=True, check=True
        )
        print(f"✅ Conexión a '{wifi_reconnect}' exitosa.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al intentar conectar a '{wifi_reconnect}': {e.output}")
        driver.quit()
        exit()

    # Esperar más tiempo para asegurarse de que la conexión se restablezca
    time.sleep(120)

    # Volver a ingresar a la IP con credenciales
    try:
        print("Reingresando a la página del módem...")
        driver.get("http://support:support@192.168.0.1")

        # Esperar a que el frame "menufrm" esté presente
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "menufrm"))
        )
        driver.switch_to.frame("menufrm")
        print("✅ Cambio al frame 'menufrm' exitoso.")
    except TimeoutException:
        print("❌ Error: No se encontró el frame 'menufrm'.")
        driver.quit()
        exit()

    # Buscar y hacer clic en "Advanced Setup"
    try:
        advanced_setup_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Advanced Setup')]"))
        )
        print("✅ Botón 'Advanced Setup' encontrado. Haciendo clic...")
        advanced_setup_button.click()
    except TimeoutException:
        print("❌ No se encontró el botón 'Advanced Setup'.")
        driver.quit()
        exit()

    # Buscar y hacer clic en el enlace "Security"
    try:
        security_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Security')]"))
        )
        print("✅ Enlace 'Security' encontrado. Haciendo clic...")
        security_link.click()
    except TimeoutException:
        print("❌ No se encontró el enlace 'Security' después de 10 segundos.")
        driver.quit()
        exit()

    # Cambiar al frame que contiene el botón "Add" en la pantalla "Outgoing IP Filtering Setup"
    try:
        driver.switch_to.default_content()  # Volver al contenido principal
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "basefrm"))
        )
        driver.switch_to.frame("basefrm")
        print("✅ Cambio al frame 'basefrm' exitoso para 'Outgoing IP Filtering Setup'.")
    except TimeoutException:
        print("❌ Error: No se encontró el frame 'basefrm' para 'Outgoing IP Filtering Setup'.")
        driver.quit()
        exit()

    # Esperar a que el botón "Add" esté presente y visible en la pantalla "Outgoing IP Filtering Setup"
    try:
        add_button_outgoing_ip = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Add']"))
        )
        print("✅ Botón 'Add' en 'Outgoing IP Filtering Setup' encontrado. Haciendo clic...")
        add_button_outgoing_ip.click()
    except TimeoutException:
        print("❌ No se encontró el botón 'Add' en 'Outgoing IP Filtering Setup' después de 10 segundos.")
        driver.quit()
        exit()

    # Esperar a que el campo "Filter Name" esté presente y visible
    try:
        filter_name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "txtfltname"))
        )
        print("✅ Campo 'Filter Name' encontrado. Ingresando valor 'ping'...")
        filter_name_field.clear()
        filter_name_field.send_keys("ping")
    except TimeoutException:
        print("❌ No se encontró el campo 'Filter Name' después de 10 segundos.")
        driver.quit()
        exit()

    # Seleccionar la opción "ICMP" en el menú desplegable "Protocol"
    try:
        protocol_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "protocol"))
        )
        print("✅ Menú desplegable 'Protocol' encontrado. Seleccionando opción 'ICMP'...")
        protocol_dropdown.click()
        protocol_option_icmp = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//select[@name='protocol']/option[@value='3']"))
        )
        protocol_option_icmp.click()
    except TimeoutException:
        print("❌ No se encontró el menú desplegable 'Protocol' o la opción 'ICMP' después de 10 segundos.")
        driver.quit()
        exit()

    # Hacer clic en "Apply/Save"
    try:
        apply_save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Apply/Save']"))
        )
        print("✅ Botón 'Apply/Save' encontrado. Haciendo clic...")
        apply_save_button.click()
    except TimeoutException:
        print("❌ No se encontró el botón 'Apply/Save' después de 10 segundos.")
        driver.quit()
        exit()

    # Esperar a que el botón "Add" esté presente y visible en la pantalla "Outgoing IP Filtering Setup"
    try:
        add_button_outgoing_ip = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Add']"))
        )
        print("✅ Botón 'Add' en 'Outgoing IP Filtering Setup' encontrado. Haciendo clic...")
        add_button_outgoing_ip.click()
    except TimeoutException:
        print("❌ No se encontró el botón 'Add' en 'Outgoing IP Filtering Setup' después de 10 segundos.")
        driver.quit()
        exit()

    # Esperar a que el campo "Filter Name" esté presente y visible
    try:
        filter_name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "txtfltname"))
        )
        print("✅ Campo 'Filter Name' encontrado. Ingresando valor 'web'...")
        filter_name_field.clear()
        filter_name_field.send_keys("web")
    except TimeoutException:
        print("❌ No se encontró el campo 'Filter Name' después de 10 segundos.")
        driver.quit()
        exit()

    # Seleccionar la opción "TCP/UDP" en el menú desplegable "Protocol"
    try:
        protocol_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "protocol"))
        )
        print("✅ Menú desplegable 'Protocol' encontrado. Seleccionando opción 'TCP/UDP'...")
        protocol_dropdown.click()
        protocol_option_tcp_udp = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//select[@name='protocol']/option[@value='0']"))
        )
        protocol_option_tcp_udp.click()
    except TimeoutException:
        print("❌ No se encontró el menú desplegable 'Protocol' o la opción 'TCP/UDP' después de 10 segundos.")
        driver.quit()
        exit()

    # Ingresar "190.13.88.0/21" en el campo "Source IP address[/prefix length]"
    try:
        source_ip_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "srcaddr"))
        )
        print("✅ Campo 'Source IP address[/prefix length]' encontrado. Ingresando valor '190.13.88.0/21'...")
        source_ip_field.clear()
        source_ip_field.send_keys("190.13.88.0/21")
    except TimeoutException:
        print("❌ No se encontró el campo 'Source IP address[/prefix length]' después de 10 segundos.")
        driver.quit()
        exit()

    # Ingresar "80" en el campo "Destination Port (port or port:port)"
    try:
        destination_port_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "dstport"))
        )
        print("✅ Campo 'Destination Port (port or port:port)' encontrado. Ingresando valor '80'...")
        destination_port_field.clear()
        destination_port_field.send_keys("80")
    except TimeoutException:
        print("❌ No se encontró el campo 'Destination Port (port or port:port)' después de 10 segundos.")
        driver.quit()
        exit()

    # Hacer clic en "Apply/Save"
    try:
        apply_save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Apply/Save']"))
        )
        print("✅ Botón 'Apply/Save' encontrado. Haciendo clic...")
        apply_save_button.click()
    except TimeoutException:
        print("❌ No se encontró el botón 'Apply/Save' después de 10 segundos.")
        driver.quit()
        exit()

    # Cambiar al frame que contiene el menú
    try:
        driver.switch_to.default_content()  # Volver al contenido principal
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "menufrm"))
        )
        driver.switch_to.frame("menufrm")
        print("✅ Cambio al frame 'menufrm' exitoso nuevamente.")
    except TimeoutException:
        print("❌ Error: No se encontró el frame 'menufrm'.")
        driver.quit()
        exit()

    # Buscar y hacer clic en "Wireless"
    try:
        wireless_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Wireless')]"))
        )
        print("✅ Botón 'Wireless' encontrado. Haciendo clic...")
        wireless_button.click()
    except TimeoutException:
        print("❌ No se encontró el botón 'Wireless'.")
        driver.quit()
        exit()

    driver.switch_to.default_content()  # Volver al contenido principal
    print("✅ Navegación a 'Wireless' exitosa.")

    # Cambiar al frame que contiene el campo "SSID"
    try:
        driver.switch_to.frame("basefrm")
        print("✅ Cambio al frame 'basefrm' exitoso para Wireless.")
    except NoSuchFrameException:
        print("❌ Error: No se encontró el frame 'basefrm' después de Wireless.")
        driver.quit()
        exit()

    # Esperar a que el campo "SSID" esté presente y visible, e ingresar el valor ingresado por el usuario
    try:
        ssid_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @name='wlSsid']"))
        )
        print("✅ Campo 'SSID' encontrado. Ingresando el nombre de la red según el usuario...")
        ssid_field.clear()
        ssid_field.send_keys(user_ssid)
        
        # Verificar que el valor ingresado en el campo SSID sea el mismo que user_ssid
        entered_value = ssid_field.get_attribute("value")
        if entered_value == user_ssid:
            print(f"✅ Verificación exitosa: el SSID ingresado es '{entered_value}'.")
        else:
            print(f"❌ Verificación fallida: el SSID ingresado es '{entered_value}' en lugar de '{user_ssid}'.")
            driver.quit()
            exit()
    except TimeoutException:
        print("❌ No se encontró el campo 'SSID' después de 10 segundos.")
        driver.quit()
        exit()

    # Seleccionar el país "ARGENTINA" en el menú desplegable "Country"
    try:
        country_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='wlCountry']"))
        )
        print("✅ Menú desplegable 'Country' encontrado. Seleccionando 'ARGENTINA'...")
        country_dropdown.click()
        country_option_argentina = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//select[@name='wlCountry']/option[@value='AR']"))
        )
        country_option_argentina.click()
    except TimeoutException:
        print("❌ No se encontró el menú desplegable 'Country' o la opción 'ARGENTINA' después de 10 segundos.")
        driver.quit()
        exit()

    # Hacer clic en "Apply/Save"
    try:
        apply_save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Apply/Save']"))
        )
        print("✅ Botón 'Apply/Save' encontrado. Haciendo clic...")
        apply_save_button.click()
    except TimeoutException:
        print("❌ No se encontró el botón 'Apply/Save' después de 10 segundos.")
        driver.quit()
        exit()

    # **** NUEVO PASO: Reconectar a la nueva red ****
    # Generar dinámicamente un perfil para la red abierta con SSID igual a user_ssid
    print(f"🔄 Preparando la conexión a la nueva red WiFi '{user_ssid}'...")
    profile_xml = f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{user_ssid}</name>
    <SSIDConfig>
        <SSID>
            <name>{user_ssid}</name>
        </SSID>
        <nonBroadcast>false</nonBroadcast>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>open</authentication>
                <encryption>none</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
        </security>
    </MSM>
</WLANProfile>
"""
    # Guardar el perfil en un archivo temporal usando encoding UTF-8
    temp_dir = tempfile.gettempdir()
    profile_path = os.path.join(temp_dir, "temp_profile.xml")
    with open(profile_path, "w", encoding="utf-8") as f:
        f.write(profile_xml)
    print(f"✅ Perfil generado en: {profile_path}")

    # Agregar el perfil a Windows
    try:
        result_add = subprocess.run(
            ["netsh", "wlan", "add", "profile", f"filename={profile_path}"],
            capture_output=True, text=True, check=True
        )
        print("✅ Perfil agregado exitosamente.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al agregar el perfil: {e.output}")
        driver.quit()
        exit()
    time.sleep(30)  #aca camie 60
        

    # Conectar a la nueva red usando el perfil agregado
    print(f"🔄 Intentando conectar a la nueva red WiFi '{user_ssid}'...")
    try:
        result_connect = subprocess.run(
            ["netsh", "wlan", "connect", f"name={user_ssid}"],
            capture_output=True, text=True, check=True
        )
        print(f"✅ Conexión a la red '{user_ssid}' exitosa.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al intentar conectar a la red '{user_ssid}': {e.output}")
        driver.quit()
        exit()

    # Eliminar el archivo temporal del perfil
    os.remove(profile_path)
    print("✅ Archivo de perfil temporal eliminado.")

    # Esperar tiempo para que la nueva conexión se estabilice
    time.sleep(30)

    # Verificar la conexión actual usando netsh
    try:
        result_status = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True, text=True, check=True
        )
        if user_ssid in result_status.stdout:
            print(f"✅ Se detectó que se conectó a la red '{user_ssid}'.")
        else:
            print(f"❌ No se detectó la conexión a la red '{user_ssid}'.")
            driver.quit()
            exit()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al verificar el estado de la conexión: {e.output}")
        driver.quit()
        exit()

    # --- NUEVO BLOQUE: Ir directo a Security en la nueva red ---
    # Esperar tiempo adicional para que la interfaz del módem se estabilice en la nueva red
    # Asumimos que la interfaz ya se cargó; forzamos el cambio al contenido principal y buscamos el frame 'menufrm'
    try:
        driver.switch_to.default_content()
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.NAME, "menufrm"))
        )
        driver.switch_to.frame("menufrm")
        print("✅ Cambio al frame 'menufrm' exitoso en la nueva conexión.")
    except TimeoutException:
        print("❌ Error: No se encontró el frame 'menufrm' en la nueva conexión.")
        # Para depuración, puedes imprimir driver.page_source aquí
        driver.quit()
        exit()

    # Buscar y hacer clic en el enlace "Security"
    try:
        # Usamos un XPATH basado en el href, ya que es estable:
        security_link = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='wlsecurity.html']"))
        )
        print("✅ Enlace 'Security' encontrado. Haciendo clic...")
        security_link.click()
    except TimeoutException:
        print("❌ No se encontró el enlace 'Security' en la nueva conexión después de 60 segundos.")
        # Para depuración, puedes imprimir driver.page_source
        driver.quit()
        exit()

    try:
        driver.switch_to.default_content()
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.NAME, "basefrm"))
        )
        driver.switch_to.frame("basefrm")
        print("✅ Cambio al frame 'basefrm' exitoso en la nueva conexión.")
    except TimeoutException:
        print("❌ Error: No se encontró el frame '' en la nbasefrmueva conexión.")
        # Para depuración, puedes imprimir driver.page_source aquí
        driver.quit()
        exit()

    # Seleccionar la opción "Mixed WPA2/WPA -PSK" en el menú desplegable "Network Authentication"
    try:
        auth_dropdown = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='wlAuthMode']"))
        )
        print("✅ Menú desplegable 'Network Authentication' encontrado. Seleccionando 'Mixed WPA2/WPA -PSK'...")
        auth_dropdown.click()
        auth_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//select[@name='wlAuthMode']/option[@value='psk psk2']"))
        )
        auth_option.click()
        print("✅ Opción 'Mixed WPA2/WPA -PSK' seleccionada.")
    except TimeoutException:
        print("❌ No se encontró el menú 'Network Authentication' o la opción 'Mixed WPA2/WPA -PSK'.")
        driver.quit()
        exit()

    # Esperar a que aparezca el campo de "WPA/WAPI passphrase" (que se hace visible tras seleccionar la opción)
    try:
        passphrase_field = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@type='password' and @name='wlWpaPsk']"))
        )
        print("✅ Campo 'WPA/WAPI passphrase' visible. Ingresando la contraseña...")
        passphrase_field.clear()
        passphrase_field.send_keys(wpa_pass)
    except TimeoutException:
        print("❌ No se encontró el campo 'WPA/WAPI passphrase' visible después de 60 segundos.")
        driver.quit()
        exit()
    time.sleep(5)

    # Esperar a que el botón "Apply/Save" esté presente y visible
    try:
        apply_save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Apply/Save']"))
        )
        print("✅ Botón 'Apply/Save' encontrado. Haciendo clic...")
        apply_save_button.click()
    except TimeoutException:
        print("❌ No se encontró el botón 'Apply/Save' después de 10 segundos.")
        driver.quit()
        exit()
    time.sleep(5)

finally:
    print("Cerrando el navegador...")
    driver.quit()
