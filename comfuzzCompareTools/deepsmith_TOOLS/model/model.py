from torch import nn


class LSTM(nn.Module):
    def __init__(self, vocab_size, output_size, embedding_size, hidden_size, n_layers, device, drop_prob=0.2):
        super(LSTM, self).__init__()

        self.output_size = output_size
        self.n_layers = n_layers
        self.hidden_dim = hidden_size

        self.embedding = nn.Embedding(vocab_size, embedding_size)
        self.lstm = nn.LSTM(embedding_size, hidden_size, n_layers, dropout=drop_prob, batch_first=True)
        self.dropout = nn.Dropout(drop_prob)
        self.fc = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.LogSoftmax(dim=1)

        self.device = device

    def forward(self, x, hidden):

        x = x.long()

        embeds = self.embedding(x)

        lstm_out, hidden = self.lstm(embeds, hidden)

        logit = self.fc(lstm_out)

        return logit, hidden

    def init_hidden(self, batch_size):
        weight = next(self.parameters()).data
        hidden = (weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().to(self.device),
                  weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().to(self.device))
        return hidden
