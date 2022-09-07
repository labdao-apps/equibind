# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, Input, Path
import inference_VS_2
import os
import yaml

class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory to make running multiple predictions efficient"""
        # not implemented right now
        # ideally setup would load: checkpoint = torch.load(args.checkpoint, map_location=device) from line 460 in inference_VS_2.py
        # self.model = torch.load("./weights.pth")

    def predict(
        self,
        protein: Path = Input(description="a PDB protein structure file"),
        small_molecule_library: Path = Input(description="an SDF file containing >=2 small molecule ligands"),
    ) -> Path:    
        """Make a prediction given an input protein and small molecule library"""
        # not implemented right now
        # ideally predict would call: inference_VS_2.predict(protein, small_molecule_library, self.model)
        # return "not implemented"

        # defining source and output directory paths after loading default arguments
        args = inference_VS_2.parse_arguments()
        args = args[0]
        args.inference_path = '/src/tmp'
        args.output_directory = '/src/out'

        # isolate the argument path basenames
        protein_base = os.path.basename(protein)
        small_molecule_library_base = os.path.basename(small_molecule_library)

        # moving files from the paths defined in the arguments to the input directory for processing
        os.system('mkdir -p ' + args.inference_path + '/dummy')
        os.system('mv ' + protein + ' ' + args.inference_path + '/dummy/protein_' + protein_base)
        os.system('mv ' + small_molecule_library + ' ' + args.inference_path + '/dummy/ligands_' + small_molecule_library_base)

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
        return(args.output_directory + '/ligands_predicted.sdf')

if __name__ == '__main__':
    p = Predictor()
    p.predict(protein = '/src/test/test.pdb', small_molecule_library = '/src/test/test.sdf')