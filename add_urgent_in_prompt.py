import json

input_file = "agentclinic_medqa.jsonl"
output_file = "agentclinic_medqa_urgent.jsonl"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        try:
            case = json.loads(line)
            osce = case.get("OSCE_Examination", {})

            # 1. 修改 Objective_for_Doctor
            if "Objective_for_Doctor" in osce:
                original_obj = osce["Objective_for_Doctor"]
                # Replace only the beginning part, preserving the symptom description
                osce["Objective_for_Doctor"] = "Rapidly " + original_obj

            # 2. 修改 History 字段（加一段话在最前）
            patient = osce.get("Patient_Actor", {})
            if "History" in patient:
                history = patient["History"]
                if not history.startswith("The patient appears visibly distressed"):
                    patient["History"] = "The patient appears visibly distressed and wants immediate care. " + history

            # 写入修改后的内容
            outfile.write(json.dumps(case, ensure_ascii=False) + "\n")

        except Exception as e:
            print("Skipping line due to error:", e)
            continue

print(f"✅ Finished writing modified data to {output_file}")
