'''
Repulsive autoencoder. This is an autoencoder that differs from a standard VAE in the following ways:

- The latent variances are not learned, they are simply set to 0.
- A normalization step takes the latent variables to a sphere surface.
- The regularization loss is changed to an energy term that
  corresponds to a pairwise repulsive force between the encoded
  elements of the minibatch.
'''

import numpy as np

from keras.layers import Input, Dense, Lambda
from keras.models import Model
from keras import backend as K
from keras import objectives


def build_model(batch_size, original_dim, intermediate_dims, latent_dim):
    x = Input(batch_shape=(batch_size, original_dim))
    h = x
    for intermediate_dim in intermediate_dims:
        h = Dense(intermediate_dim, activation='relu')(h)

    # Completely got rid of the variational aspect
    z_unnormalized = Dense(latent_dim)(h)

    # normalize all latent vars:
    z = Lambda(lambda z_unnormed: K.l2_normalize(z_unnormed, axis=-1))([z_unnormalized])

    # we instantiate these layers separately so as to reuse them both for reconstruction and generation
    decoder_input = Input(shape=(latent_dim,))
    h_decoded = z
    _h_decoded = decoder_input
    for intermediate_dim in reversed(intermediate_dims):
        decoder_h = Dense(intermediate_dim, activation='relu')
        h_decoded = decoder_h(h_decoded)    
        _h_decoded = decoder_h(_h_decoded)

    decoder = Dense(original_dim, activation='sigmoid')
    x_decoded = decoder(h_decoded)
    _x_decoded = decoder(_h_decoded)

    def vae_loss(x, x_decoded):
#        mse_loss = original_dim * objectives.mean_squared_error(x, x_decoded)
        xent_loss = original_dim * objectives.binary_crossentropy(x, x_decoded)
        # Instead of a KL normality test, here's some energy function
        # that pushes the minibatch elements away from each other, pairwise.
        # pairwise = K.sum(K.square(K.dot(z, K.transpose(z))))

#        epsilon = 0.0001
#        distances = (2.0 + epsilon - 2.0 * K.dot(z, K.transpose(z))) ** 0.5
#        regularization = -K.mean(distances) * 100 # Keleti
        # regularization = K.mean(1.0 / distances) * 100 # Coulomb
#        return xent_loss + regularization
        return xent_loss

    rae = Model(x, x_decoded)
    rae.compile(optimizer='rmsprop', loss=vae_loss)

    # build a model to project inputs on the latent space
    encoder = Model(x, z)

    # build a digit generator that can sample from the learned distribution
    generator = Model(decoder_input, _x_decoded)

    return rae, encoder, generator


# Taken uniformly from sphere in R^latentdim
def sample(batch_size, latent_dim):
    z_sample = np.random.normal(size=(batch_size, latent_dim))
    z_sample /= np.linalg.norm(z_sample)
    return z_sample
