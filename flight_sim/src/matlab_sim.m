max_velocity = 800;
wing_area = 5825;
max_altitude = 45100;
act_dynamics = 0.25;

% #time parameters
resolution = 0.01;
time = 0;
sim_time = 100;
iter = 1;

% #throttle position simulation
throttle_pos = [];
i = 0;
prev_throttle_pos = 0;
prev_max_velocity = 0;
count = 1;
sim_up = 0;

% #velocity calculation
% #throttle_pos = get throttle position from keyboard or joystick

while i<=sim_time
      if i > 0 && i <= 0.2*sim_time
          throttle_pos(count) = 0.1;
      elseif i > 0.2*sim_time && i <= 0.4*sim_time
          throttle_pos(count) = 0.3;
      elseif i > 0.4*sim_time && i <= 0.5*sim_time
          throttle_pos(count) = 0.6;
      elseif i > 0.5*sim_time && i <= 0.75*sim_time
          throttle_pos(count) = 0.8;
      else
          throttle_pos(count) = 1;
      end
%       throttle_pos(count) = 0.3;
      i = i+resolution;
      count = count + 1;
end
while sim_up < 1
      if iter == length(throttle_pos)
            sim_up = 1;
      end
          
      if iter == 1
            prev_throttle_pos = throttle_pos(iter);
      end
            
      if prev_throttle_pos == throttle_pos(iter)
            time = time + resolution;
      else
            time = 0;
            prev_max_velocity = max_velocity*prev_throttle_pos;
      end
          
      sat_velocity = max_velocity*throttle_pos(iter);
      velocity_func = act_dynamics*time;
      velocity = prev_max_velocity + sat_velocity*(velocity_func)^2;
      if velocity >= sat_velocity
           velocity = sat_velocity;
      end
      y_axis(iter) = velocity;
      x_axis(iter) = iter*resolution;
      prev_throttle_pos = throttle_pos(iter);
      iter = iter + 1;
%       velocity = (velocity/max_velocity)*(-180-110)
end

plot(x_axis,y_axis);
    