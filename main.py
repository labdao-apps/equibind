import sys 
import inference_VS_2
import os
import yaml
# import fastapi # a package we use to receive and return results via an API

def predict(args):
    # isolate the argument path basenames
    protein_base = os.path.basename(args.protein)
    small_molecule_library_base = os.path.basename(args.small_molecule_library)
    # defining file name
    protein_destination = args.inference_path + '/dummy/' + protein_base
    small_molecule_library_destination = args.inference_path + '/dummy/' + small_molecule_library_base
    # moving files from the paths defined in the arguments to the input directory for processing
    print("moving files to " + args.inference_path + " for processing")
    os.system('mkdir -p ' + args.inference_path + '/dummy')
    os.system('cp ' + args.protein + ' ' + protein_destination)
    os.system('cp ' + args.small_molecule_library + ' ' + small_molecule_library_destination)
    # renaming file names to match the expected input pattern
    print("renaming file names to match the expected input pattern")
    os.system('mv ' + protein_destination + ' ' + args.inference_path + '/dummy/protein_' + protein_base)
    os.system('mv ' + small_molecule_library_destination + ' ' + args.inference_path + '/dummy/ligands_' + small_molecule_library_base)
    # the dataurl go package does not like .sdf files, the input should be given in .txt - something to add to petri
    #small_molecule_library_sdf = os.path.splitext(small_molecule_library_destination)[0]+'.sdf'
    #print("converting library to sdf: " + small_molecule_library_sdf)
    #os.system('mv ' + small_molecule_library_destination + ' ' + small_molecule_library_sdf)
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
    output_name = os.listdir(args.output_directory + '/dummy')[0]
    output_path_sdf = args.output_directory + '/dummy/' + output_name
    print(output_path_sdf)
    # the dataurl go package does not like .sdf files, the input should be given in .txt - something to add to petri
    # output_path = os.path.splitext(output_path_sdf)[0]+'.txt'
    # print("converting library to txt: " + output_path)
    output_path = args.output_directory + '/' + output_name
    os.system('mv ' + output_path_sdf + ' ' + output_path)
    # output
    # output = Path(output_path)
    print(output_path)
    return(output_path)

def parse_arguments_main(): 
    print("parsing arguments")
    # parsing arguments
    args = inference_VS_2.parse_arguments()
    args = args[0]
    # setting a custom default
    args.inference_path = '/src/tmp' # copy the input files to this directory for renaming and processing
    args.output_directory = '/outputs'
    print("received input: " + args.protein + " " + args.small_molecule_library + " for protein and small molecule library, respectively")
    return(args)

if __name__ == "__main__":
    args = parse_arguments_main()
    print("printing arguments:")
    print("####################")
    print(args)
    print("####################")
    print("running prediction:")
    predict(args)