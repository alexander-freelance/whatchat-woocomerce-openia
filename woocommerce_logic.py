from woocommerce import API
import logging

def create_order(store_url, consumer_key, consumer_secret, order_data):
    wcapi = API(
        url=store_url,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        version="wc/v3"
    )
    try:
        response = wcapi.post("orders", data=order_data)
        return response.json()
    except Exception as e:
        logging.error(f"Error creating order: {e}")
        return None

def get_order(store_url, consumer_key, consumer_secret, order_id=None, phone=None, email=None):
    wcapi = API(
        url=store_url,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        version="wc/v3"
    )
    
    try:
        if order_id:
            # Consulta específica por ID de pedido
            response = wcapi.get(f"orders/{order_id}")
            response.raise_for_status()
            return response.json()
        elif phone or email:
            # Utilizar el parámetro 'search' para buscar por teléfono o correo electrónico
            search_query = ""
            if phone:
                search_query += phone + " "
            if email:
                search_query += email
            search_query = search_query.strip()
            
            if not search_query:
                logging.error("Se debe proporcionar al menos un parámetro de búsqueda (order_id, phone o email).")
                return None
            
            params = {
                'search': search_query,
                'per_page': 100  # Ajusta según sea necesario
            }
            
            response = wcapi.get("orders", params=params)
            response.raise_for_status()
            orders = response.json()
            
            if orders:
                # Filtrar los pedidos para encontrar coincidencias exactas
                for order in orders:
                    match = False
                    if phone:
                        order_phone = order.get('billing', {}).get('phone', '').strip()
                        if order_phone == phone:
                            match = True
                    if email:
                        order_email = order.get('billing', {}).get('email', '').strip().lower()
                        if order_email == email.lower():
                            match = True
                    if match:
                        return order  # Retornar el primer pedido que coincida exactamente
                # Si no se encuentra una coincidencia exacta, retornar el primero de la búsqueda
                return orders[0]
            else:
                return None
        else:
            logging.error("Se debe proporcionar al menos uno de los parámetros: order_id, phone o email.")
            return None
    except Exception as e:
        logging.error(f"Error obteniendo el pedido: {e}")
        return None
    
def search_products(store_url, consumer_key, consumer_secret, search_query):
    wcapi = API(
        url=store_url,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        version="wc/v3"
    )
    try:
        response = wcapi.get("products", params={"search": search_query, "per_page": 1})
        response.raise_for_status()  # Asegura que se manejen errores HTTP
        return response.json()
    except Exception as e:
        logging.error(f"Error searching products: {e}")
        return None