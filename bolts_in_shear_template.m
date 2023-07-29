force = ; %enter the applied force/load -- make sure to convert units if necessary
yield_fail = ; %enter the failure point for the material -- make sure to convert units if necessary
diameter_in = [0.086 0.112 0.125 0.138 0.164 0.19 0.25 0.3125 0.375 0.4375 0.5 0.5625 0.625 0.75 0.875 1]; %common bolt diameters in SI
diameter_m = diameter_in .* 0.0254; %common bolt diameters in metric

shear_stress = (4 * force) ./ (pi .* (diameter_m .^ 2)); %calculate the shear stress
%shear_stress = shear_stress ./ num_shear; %if in double shear or more, uncomment here
%shear_stress = shear_stress ./ num_bolts; %if more than one bolt, uncomment here
FOS = (yield_fail ./ shear_stress) .* 0.6; %calculate the FOS, 0.6 is used for knockdown

%display the the diameter and its corresponding FOS
data = [diameter_in' shear_stress' FOS'];
variables = {'Diameter (in)', 'Shear Stress(Pa)', 'FOS'};
table(data(:,1), data(:,2), data(:,3), 'VariableNames',variables)