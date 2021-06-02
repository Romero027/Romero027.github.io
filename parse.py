import json, os, csv, pickle

with open("coqa-train-v1.0.json", "rb") as fin:
    train = json.load(fin)

with open("coqa-dev-v1.0.json", "rb") as fin:
    dev = json.load(fin)

client_list = {}
for qa in train['data']:
    id = qa['id']
    num_samples = len(qa['questions'])
    if num_samples < 8:
        continue
    client_list[id] = qa

for qa in dev['data']:
    id = qa['id']
    num_samples = len(qa['questions'])
    if num_samples < 8:
        continue
    client_list[id] = qa

client_ids = list(client_list.keys())

ratios = [(0.8, 'train'), (0.05, 'val'), (0.15, 'test')]
base_index = 0

for ratio, folder in ratios:
    temp_index = base_index
    if not os.path.isdir(folder):
        os.makedirs(folder, exist_ok=True)

    results = [['client_id', 'data_path', 'label_name', 'label_id']]
    client_idx = 0
    for i in range(temp_index, temp_index+int(ratio*len(client_ids))):
        for sample in client_list[client_ids[i]]['answers']:
            results.append([client_idx, folder+'/'+str(client_ids[i]), sample['input_text'], "-1"])

            # move data
            with open(folder+'/'+str(client_ids[i]), "wb") as fout:
                pickle.dump(sample, fout)

        client_idx += 1
        base_index += 1

    csv_output = 'client_data_mapping/'+folder+'.csv'
    with open(csv_output, "w") as fout:
        writer = csv.writer(fout, delimiter=',')
        #writer.writerow(['client_id' , 'data_path' , 'label_name', 'label_id'])
        for r in results:
            writer.writerow(r)

