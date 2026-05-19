"""Project-wide settings and constants.

Changing model settings here should not require editing the UI.
For example, if KNN with k=3 performs better, change KNN_K_VALUE to 3 here.
"""

DATASET_FILE = "intrusion_dataset.csv"
SAMPLE_FILE = "sample_intrusion_dataset.csv"

# Main model settings
MLP_HIDDEN_LAYERS = (64, 32, 16, 8, 4)
MLP_MAX_ITER = 500
MLP_RANDOM_STATE = 42
KNN_K_VALUE = 3 
TEST_SIZE = 0.25
RANDOM_STATE = 42

IMPORTANT_FEATURES = {
    "duration": "Length of the connection in seconds.",
    "protocol_type": "Network protocol used, such as TCP, UDP, or ICMP.",
    "service": "Network service being accessed, for example HTTP, FTP, Telnet, or private.",
    "flag": "Connection status. SF usually means successful; S0/REJ often means failed or rejected.",
    "src_bytes": "Bytes sent from source to destination.",
    "dst_bytes": "Bytes sent from destination back to source.",
    "logged_in": "1 means login succeeded, 0 means not logged in.",
    "num_failed_logins": "Number of failed login attempts.",
    "count": "Recent connections from the same source to the same host.",
    "srv_count": "Recent connections to the same service.",
    "serror_rate": "Rate of SYN/connection setup errors.",
    "srv_serror_rate": "SYN error rate for the same service.",
    "rerror_rate": "Rejected connection error rate.",
    "srv_rerror_rate": "Rejected connection error rate for the same service.",
    "same_srv_rate": "Rate of connections to the same service.",
    "diff_srv_rate": "Rate of connections to different services.",
    "dst_host_count": "Recent connections to the destination host.",
    "dst_host_srv_count": "Recent connections to the destination host using the same service.",
    "dst_host_same_srv_rate": "How often destination host connections use the same service.",
    "dst_host_diff_srv_rate": "How often destination host connections use different services.",
}

FEATURE_GROUPS = {
    "Basic connection info": ["duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes"],
    "Login behavior": ["logged_in", "num_failed_logins"],
    "Traffic volume": ["count", "srv_count", "dst_host_count", "dst_host_srv_count"],
    "Error rates": ["serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate"],
    "Service pattern rates": ["same_srv_rate", "diff_srv_rate", "dst_host_same_srv_rate", "dst_host_diff_srv_rate"],
}

BASE_PROFILES = {
    "Normal Web Browsing": {"duration":0,"protocol_type":"tcp","service":"http","flag":"SF","src_bytes":240,"dst_bytes":3200,"logged_in":1,"count":10,"srv_count":10,"serror_rate":0.0,"srv_serror_rate":0.0,"rerror_rate":0.0,"srv_rerror_rate":0.0,"same_srv_rate":1.0,"diff_srv_rate":0.0,"dst_host_count":30,"dst_host_srv_count":30,"dst_host_same_srv_rate":1.0,"dst_host_diff_srv_rate":0.0},
    "DoS / Flood Attack": {"duration":0,"protocol_type":"tcp","service":"private","flag":"S0","src_bytes":0,"dst_bytes":0,"logged_in":0,"count":280,"srv_count":5,"serror_rate":1.0,"srv_serror_rate":1.0,"rerror_rate":0.0,"srv_rerror_rate":0.0,"same_srv_rate":0.02,"diff_srv_rate":0.10,"dst_host_count":255,"dst_host_srv_count":5,"dst_host_same_srv_rate":0.02,"dst_host_diff_srv_rate":0.10},
    "Probe / Scanning": {"duration":0,"protocol_type":"tcp","service":"private","flag":"REJ","src_bytes":0,"dst_bytes":0,"logged_in":0,"count":150,"srv_count":25,"serror_rate":0.0,"srv_serror_rate":0.0,"rerror_rate":1.0,"srv_rerror_rate":1.0,"same_srv_rate":0.15,"diff_srv_rate":0.08,"dst_host_count":255,"dst_host_srv_count":25,"dst_host_same_srv_rate":0.09,"dst_host_diff_srv_rate":0.08},
    "Suspicious Login Attempt": {"duration":0,"protocol_type":"tcp","service":"telnet","flag":"SF","src_bytes":129,"dst_bytes":174,"logged_in":0,"num_failed_logins":1,"count":1,"srv_count":1,"serror_rate":0.0,"srv_serror_rate":0.0,"rerror_rate":0.0,"srv_rerror_rate":0.0,"same_srv_rate":1.0,"diff_srv_rate":0.0,"dst_host_count":1,"dst_host_srv_count":1,"dst_host_same_srv_rate":1.0,"dst_host_diff_srv_rate":0.0},
}
