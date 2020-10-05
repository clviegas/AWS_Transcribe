'''
Xinru Yan
Oct 2020

Post processing script for amazon transcribe return
'''
import json, glob, os
import click


@click.command()
@click.option('-i', '--input_dir', default='/Users/xinruyan/Developer/elizabethhau_emilyahn-finalproject/data/amazon_output/', type=str)
def main(input_dir):
    for jsonfile in glob.glob(os.path.join(input_dir, '*.json')):
        with open(jsonfile, 'rb') as f:
            data = json.load(f)
            jobname = data['jobName']
            print(f'file {jobname}')
            print(data['results']['transcripts'][0]['transcript'])
            print('\n\n')
            #print(data['results'])


if __name__ == "__main__":
    main()