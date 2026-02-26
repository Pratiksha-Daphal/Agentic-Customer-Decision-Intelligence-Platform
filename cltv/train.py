import pandas as pd
from pathlib import Path
import torch
from torch.utils.data import DataLoader, TensorDataset
from .model import CLTVModel

# Load data from package directory
data_path = Path(__file__).resolve().parent / "cltv_training_data.csv"
df = pd.read_csv(data_path)

X = df.drop(columns=["customer_id", "cltv_label"]).values
y = df["cltv_label"].values

X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.float32)

dataset = TensorDataset(X, y)
loader = DataLoader(dataset, batch_size=64, shuffle=True)

model = CLTVModel(input_dim=X.shape[1])
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = torch.nn.MSELoss()

for epoch in range(20):
    for xb, yb in loader:
        pred = model(xb)
        loss = loss_fn(pred, yb)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"Epoch {epoch}: loss={loss.item():.4f}")

torch.save(model.state_dict(), "cltv_model.pt")