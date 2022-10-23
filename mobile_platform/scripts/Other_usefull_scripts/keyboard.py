#Author: Fredys Garces Olivares

from pynput import keyboard as kb
import rclpy
from rclpy.node import Node

class TestParams(Node):
    def __init__(self):
        super().__init__('test_params_rclpy')
        self.declare_parameter('seguidor_de_linea')
        self.declare_parameter('giro_derecha')
        self.declare_parameter('giro_izquierda')
        self.declare_parameter('objeto_detectado')
        
#****************************************************************

        def pulsa(tecla):
            if tecla == kb.KeyCode.from_char('1'):
                print('Se ha pulsado la tecla ' + str(tecla)+'\n'+'Aquí va el codigo para que vaya a la habitación 1')
                self.declare_parameter('seguidor_de_linea', True)
                
                    
            if tecla == kb.KeyCode.from_char('2'):
                print('Se ha pulsado la tecla ' + str(tecla)+'\n'+'Aquí va el codigo para que vaya a la habitación 2') 
                self.declare_parameter('seguidor_de_linea', True)

        with kb.Listener(pulsa) as listener:
            listener.join()

#****************************************************************



#****************************************************************
# The following is just to start the node
def main(args=None):
    rclpy.init(args=args)
    node = TestParams()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
if __name__ == "__main__":
    main()
