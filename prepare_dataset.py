import pandas as pd
from pathlib import Path

NSL_COLUMNS = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins",
    "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root",
    "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds",
    "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate",
    "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate",
    "diff_srv_rate", "srv_diff_host_rate", "dst_host_count",
    "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate",
    "dst_host_srv_rerror_rate", "attack_type", "difficulty"
]

DOS = {"back", "land", "neptune", "pod", "smurf", "teardrop", "apache2", "udpstorm", "processtable", "mailbomb"}
PROBE = {"ipsweep", "nmap", "portsweep", "satan", "mscan", "saint"}
R2L = {"ftp_write", "guess_passwd", "imap", "multihop", "phf", "spy", "warezclient", "warezmaster", "sendmail", "named", "snmpgetattack", "snmpguess", "xlock", "xsnoop", "worm"}
U2R = {"buffer_overflow", "loadmodule", "perl", "rootkit", "httptunnel", "ps", "sqlattack", "xterm"}

def map_attack_category(label):
    label = str(label).strip().replace(".", "")      # converting to string and cleanig
    if label == "normal": return "normal"
    if label in DOS: return "dos"
    if label in PROBE: return "probe"
    if label in R2L: return "r2l"
    if label in U2R: return "u2r"
    return "attack"        # if unknown mark as attack

def prepare_nsl_kdd(input_file="KDDTrain+.txt", output_file="intrusion_dataset.csv"):
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"{input_file} not found. Put KDDTrain+.txt in this folder first.")

    df = pd.read_csv(input_path, header=None, names=NSL_COLUMNS)
    df["attack_type"] = df["attack_type"].astype(str).str.replace(".", "", regex=False).str.strip()
    df["label"] = df["attack_type"].apply(lambda x: "normal" if x == "normal" else "attack")    # if attack type normal set normal, else attack
    df["attack_category"] = df["attack_type"].apply(map_attack_category)   # map attacks based on category (dos, probe, normal)
    df.to_csv(output_file, index=False)

    print("Dataset prepared successfully.")
    print(f"Saved as: {output_file}")
    print(f"Rows: {len(df)}")
    print(df["label"].value_counts())

if __name__ == "__main__":
    prepare_nsl_kdd()
