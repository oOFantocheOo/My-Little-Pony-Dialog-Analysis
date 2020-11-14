Dependencies:

  pandas
  

General instructions:

  Run  `python <source_csv_file> -o <output_json_path>` to see the analysis in json format. This assumes words_alpha.txt is sitting at data/.
  This should conduct an analysis on verbosity, mentions, follow-on comments and top 5 non-dictionary words used by the 5 protagonists.
  Here -o <output_json_path> is optional. If not provided, the output will be printed to stdout directly.
  The format of <source_csv_file> is expected to be the same with data/clean_dialog.csv.


Demo instructions:

  After cloning the repository (assuming data/clean_dialog.csv is provided), run `python data/clean_dialog.csv -o result.json` to see the result in result.json, or run `python data/clean_dialog.csv` to see output in stdout.
  

Please refer to homework 03.pdf for more details
