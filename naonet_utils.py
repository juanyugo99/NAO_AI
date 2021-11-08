import numpy as np
import torch
from torch import nn

# Network Definition
class Net(torch.nn.Module):
  def __init__(self, n_feature, n_hidden, n_output, n_layers, activ_func):
    super(Net, self).__init__()

    activation_list = {"relu": nn.ReLU , "tanh": nn.Tanh , "sigmoid": nn.Sigmoid}
    
    # input layer
    layers = [nn.Linear(n_feature, n_hidden), activation_list.get(activ_func.lower())()]
      
    # Hidden Layers
    for i in range(0, n_layers):
      layers += [nn.Linear(n_hidden, n_hidden), activation_list.get(activ_func.lower())()] 

    # output layer
    layers += [nn.Linear(n_hidden, n_output), activation_list.get(activ_func.lower())()]

    self.net_layers = nn.Sequential(*layers)

  def forward(self, x): # linear output
    return self.net_layers(x)

  def forward(self, x):         # linear output
  
      return self.net_layers(x)


# import model
def import_net(config_file, features, outputs):
    checkpoint = torch.load(config_file)
    no_neurons_sel = checkpoint["neuron"]
    no_layers_sel = checkpoint["layers"]
    activation_sel = checkpoint["activation"]
    model = Net(n_feature=features, n_hidden=no_neurons_sel , n_output=outputs, n_layers =no_layers_sel, activ_func=activation_sel)
    model.load_state_dict(checkpoint["model"])
    return model
