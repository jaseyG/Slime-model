   #updating particle direction
    def update_particle_no_velo_change(self, particles): 
        x = self.position[0] + self.velocity[0] + W() * self.a_vel[0] + I() * self.avg_velocity[0]
        y = self.position[1] + self.velocity[1] + W() * self.a_vel[1] + I() * self.avg_velocity[1]
        
        #adding in hard boundary conditions
        if x < 0 or x > length:
            self.velocity = (-self.velocity[0], -self.velocity[1])
        if y < 0 or y > length:
            self.velocity = (-self.velocity[0], -self.velocity[1])
        
        if self.avg_velocity == (0, 0):
            self.avg_velocity = self.a_vel
        self.position = (x, y)
        
         #adding in hard boundary conditions
        #if x < 0 or x > length:
            #self.velocity = (-self.velocity[0], -self.velocity[1])
        #if y < 0 or y > length:
            #self.velocity = (-self.velocity[0], -self.velocty[1])
              
def update_particle_no_base_velo(self, particles):
    vx_new = W * self.attraction_velocity_influence[0] + I * self.avg_n_velocity[0] + random.uniform(-0.5, 0.5)
    vy_new = W * self.attraction_velocity_influence[1] + I * self.avg_n_velocity[1] + random.uniform(-0.5, 0.5)
    magnitude = math.sqrt(vx_new**2 + vy_new**2)
    if magnitude > max_velocity:
        scale = max_velocity / magnitude
        vx_new *= scale
        vy_new *= scale
    self.velocity = (vx_new, vy_new) 
    x = self.position[0] + self.velocity[0]
    y = self.position[1] + self.velocity[1]
    self.position = (x, y)