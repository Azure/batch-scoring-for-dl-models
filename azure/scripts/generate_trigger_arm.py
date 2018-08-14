import json
import argparse 
import os
import jinja2

if __name__ == "__main__":
  # set up parser
  parser = argparse.ArgumentParser( \
    description='Generate the Logic App & ACI  \
    template for deployment.')
  parser.add_argument(
    'output',
    help='The path of the output json file.'
  )

  args = parser.parse_args()
  json_output = args.output

  # use jinja to fill in variables from .env file
  path = os.path.dirname(os.path.abspath(__file__))
  env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
      os.path.join(path, '../arm')
    )
  )
  template = env.get_template('template.trigger_arm.json')

  e = os.environ
  rendered_template = template.render(env=e)

  out = open(json_output, 'w')
  out.write(rendered_template)
  out.close()

