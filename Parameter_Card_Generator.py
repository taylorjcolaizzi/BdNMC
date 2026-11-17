import subprocess as subp

def update_param(b,replacement_dictionary):
    for i in range(len(b)):
        line = b[i].split()
        if len(line)<2:
            continue
        if line[0] in replacement_dictionary:
            b[i]=line[0]+' '+str(replacement_dictionary[line[0]])+'\n'
    return b

def update_production_channels(lines, channels):
    updated = []
    inserted_channels = False

    for line in lines:
        fields = line.split()
        if fields and fields[0] == "production_channel":
            if not inserted_channels:
                for channel_entry in channels:
                    channel, distribution = channel_entry[:2]
                    updated.append(f"production_channel {channel}\n")
                    updated.append(f"production_distribution {distribution}\n")
                    if len(channel_entry) > 2:
                        for key, value in channel_entry[2].items():
                            updated.append(f"{key} {value}\n")
                inserted_channels = True
            continue
        if fields and fields[0] == "production_distribution":
            continue
        updated.append(line)

    if not inserted_channels:
        raise ValueError("No production_channel entries found in the parameter card.")
    if not channels:
        raise ValueError("At least one production channel must be enabled.")
    return updated

#file is the parameter card you're reading in, outfile is the name for the new parameter card you're generating
#replacement dictionary is the list of parameters you want to change.
#This will also run the paramter file if run=True!
def run_output_file(file,outfile,replacement_dictionary,run=True,production_channels=None):
    with open(file) as f:
        b=f.readlines()
    b=update_param(b,replacement_dictionary)
    if production_channels is not None:
        b=update_production_channels(b,production_channels)
    with open(outfile,'w') as f:
            f.writelines(b)
    if run:
        subp.call(["./bin/BDNMC", outfile])

#A sample script for iterating over dark photon masses with the sample parameter file.
def test():
    mdp_list={0.05,0.1,0.15}
    for mdp in mdp_list:
    	eps=1e-3
    	alpha_D=0.5
    	mdm=mdp/3
    	out_prepend="test_events"

    	replacement_dictionary={"epsilon" : eps, "alpha_D" : alpha_D, "dark_photon_mass" : mdp , "dark_matter_mass" : mdm, "output_file" : out_prepend+"_{}gev.dat".format(mdp)}

    	run_output_file("parameter.dat", "parameter_run.dat", replacement_dictionary)

if __name__ == "__main__":
	test()
