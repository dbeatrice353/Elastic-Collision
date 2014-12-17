from vector import Vector2
import math

def dot_product(v1,v2):
    return v1.x*v2.x + v1.y*v2.y

def quadratic_formula(a,b,c):
    if a == 0:
        return [0,0]
    desc = (b*b - 4*a*c)
    if desc >= 0:
        desc = desc**(1/2)
        return [(-b+desc)/(2*a),(-b-desc)/(2*a)]
    else:
        return [0,0]

def manage_wall_contact(obj,screen_width,screen_length):
    if obj.position.x + obj.radius > screen_width:
        obj.velocity.x *= -1
        obj.position.x = screen_width - obj.radius - 1
        
    if obj.position.x - obj.radius < 0:
        obj.velocity.x *= -1
        obj.position.x = obj.radius + 1
        
    if obj.position.y + obj.radius > screen_length:
        obj.velocity.y *= -1
        obj.position.y = screen_length - obj.radius - 1

    if obj.position.y - obj.radius < 0:
        obj.velocity.y *= -1
        obj.position.y = obj.radius + 1

def peer_contact(obj1,obj2):
    distance = ((obj1.position.x - obj2.position.x)**2 + (obj1.position.y - obj2.position.y)**2)**(1/2)
    if distance < obj1.radius + obj2.radius:
        return True
    else:
        return False
    
def peer_collision(obj1,obj2):
    v1 = obj1.get_velocity()
    v2 = obj2.get_velocity()
    p1 = obj1.get_position()
    p2 = obj2.get_position()
    m1 = obj1.mass
    m2 = obj2.mass
    
    unit_norm = p2 - p1
    unit_norm.normalize()
    unit_tan = Vector2(-unit_norm.y,unit_norm.x)

    v1n = dot_product(unit_norm,v1)
    v1t = dot_product(unit_tan,v1)
    v2n = dot_product(unit_norm,v2)
    v2t = dot_product(unit_tan,v2)

    v1t_prime_scal = v1t
    v2t_prime_scal = v2t

    v1n_prime_scal = (v1n*(m1 - m2) + 2*m2*v2n)/(m1 + m2)
    v2n_prime_scal = (v2n*(m2 - m1) + 2*m1*v1n)/(m1 + m2)

    v1n_prime = v1n_prime_scal*unit_norm
    v1t_prime = v1t_prime_scal*unit_tan
    v2n_prime = v2n_prime_scal*unit_norm
    v2t_prime = v2t_prime_scal*unit_tan

    v1_prime = v1n_prime + v1t_prime
    v2_prime = v2n_prime + v2t_prime

    obj1.set_velocity(v1_prime)
    obj2.set_velocity(v2_prime)

    # Check if balls have overlapped each other. 
    v1 = v1_prime
    v2 = v2_prime
    norm = p1 - p2
    distance = norm.get_magnitude()
    overlap = obj2.radius + obj1.radius - distance
    if overlap > 0:
        # Re-set the positions so the balls don't get stuck, by passing a small amount of time for the two balls.
        a = (v1-v2).get_magnitude()**2
        b = dot_product(p1-p2,v1-v2)
        c = (p1-p2).get_magnitude()**2 - (obj2.radius + obj1.radius)**2
        solutions = quadratic_formula(a,b,c)
        if solutions[0] > 0:
            delta_t = solutions[0]
        else:
            delta_t = solutions[1]
        obj1.update(delta_t)
        obj2.update(delta_t)

def mouse_contact(mouse,obj):
    distance = ((obj.position.x - mouse.px)**2 + (obj.position.y - mouse.py)**2)**(1/2)
    if distance < obj.radius + mouse.radius:
        return True
    else:
        return False
    
def mouse_collision(mouse,obj):
    v1 = Vector2(mouse.vx,mouse.vy)
    v2 = obj.get_velocity()
    p1 = Vector2(mouse.px,mouse.py)
    p2 = obj.get_position()
    m1 = mouse.mass
    m2 = obj.mass
    
    unit_norm = p2 - p1
    unit_norm.normalize()
    unit_tan = Vector2(-unit_norm.y,unit_norm.x)

    v1n = dot_product(unit_norm,v1)
    v2n = dot_product(unit_norm,v2)
    v2t = dot_product(unit_tan,v2)

    v2t_prime_scal = v2t
    v2n_prime_scal = (v2n*(m2 - m1) + 2*m1*v1n)/(m1 + m2)
    v2n_prime = v2n_prime_scal*unit_norm
    v2t_prime = v2t_prime_scal*unit_tan
    v2_prime = v2n_prime + v2t_prime

    obj.set_velocity(v2_prime)

    v2 = v2_prime
    norm = p1 - p2
    distance = norm.get_magnitude()
    overlap = obj.radius + mouse.radius - distance
    obj.position -= (norm/distance)*overlap
    
