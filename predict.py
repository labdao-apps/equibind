# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, Input, Path
import sys
# custom changes
import inference_VS_2
import os
import yaml


class Predictor(BasePredictor):
    def predict(
        self,
        protein: Path = Input(description="a PDB protein structure file"),
        small_molecule_library: Path = Input(description="an SDF file containing >=2 small molecule ligands"),
    ) -> Path:    
        # custom changes
        args = inference_VS_2.parse_arguments()
        args = args[0]
        args.inference_path = '/src/tmp'
        args.output_directory = '/src/out'

        # formatting input
        protein = str(protein)
        small_molecule_library = str(small_molecule_library)     

        # isolate the argument path basenames
        protein_base = os.path.basename(protein)
        small_molecule_library_base = os.path.basename(small_molecule_library)

        # defining file name
        protein_destination = args.inference_path + '/dummy/protein_' + protein_base
        small_molecule_library_destination = args.inference_path + '/dummy/ligands_' + small_molecule_library_base

        # moving files from the paths defined in the arguments to the input directory for processing
        os.system('mkdir -p ' + args.inference_path + '/dummy')
        os.system('mv ' + protein + ' ' + protein_destination)
        os.system('mv ' + small_molecule_library + ' ' + small_molecule_library_destination)

        # the dataurl go package does not like .sdf files, the input should be given in .txt - something to add to petri
        small_molecule_library_sdf = os.path.splitext(small_molecule_library_destination)[0]+'.sdf'
        print("converting library to sdf: " + small_molecule_library_sdf)
        os.system('mv ' + small_molecule_library_destination + ' ' + small_molecule_library_sdf)

        # adding missings args, only works for one run_dir
        args.multi_ligand = True
        # args.model_parameters['noise_initial'] = 0

        # running the inference - this is the main function - lifted from __main__ in inference_VS_2.py
        if args.config:
            config_dict = yaml.load(args.config, Loader=yaml.FullLoader)
            arg_dict = args.__dict__
            for key, value in config_dict.items():
                if isinstance(value, list):
                    for v in value:
                        arg_dict[key].append(v)
                # dropping comparisson with CMD line arguments
                #else:
                #    if key in cmdline_args:
                #        continue
                #    arg_dict[key] = value
            args.config = args.config.name
        else:
            config_dict = {}
        

        for run_dir in args.run_dirs:
            args.checkpoint = f'runs/{run_dir}/best_checkpoint.pt'
            config_dict['checkpoint'] = f'runs/{run_dir}/best_checkpoint.pt'
            # overwrite args with args from checkpoint except for the args that were contained in the config file
            arg_dict = args.__dict__
            with open(os.path.join(os.path.dirname(args.checkpoint), 'train_arguments.yaml'), 'r') as arg_file:
                checkpoint_dict = yaml.load(arg_file, Loader=yaml.FullLoader)
            for key, value in checkpoint_dict.items():
                if (key not in config_dict.keys()):
                    if isinstance(value, list):
                        for v in value:
                            arg_dict[key].append(v)
                    else:
                        arg_dict[key] = value
            args.model_parameters['noise_initial'] = 0
            if args.inference_path == None:
                inference_VS_2.inference(args)
            elif args.multi_ligand == True:
                print('Running Multi-Ligand')
                #print(args)
                inference_VS_2.multi_lig_inference(args)
            else:
                inference_VS_2.inference_from_files(args)

        # moving the output file to the output directory
        ouput_name = os.listdir(args.output_directory)[0]
        print(ouput_name)

        return(args.output_directory + ouput_name)

if __name__ == '__main__':
    p = Predictor()
    p.predict(protein = '/src/test/test.pdb', small_molecule_library =  '/src/test/test.sdf')
    
    # print(sys.argv[0])
    # print(sys.argv[1])
    # p.predict(protein = sys.argv[0], small_molecule_library =  sys.argv[1])
    
    # '/src/test/test.pdb'
    # '/src/test/test.sdf'