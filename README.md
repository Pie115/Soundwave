This is a music recommender made for Citrus Hack 2023

## Sound Wave

Have you ever felt disapointed with your music recommendations. Do you feel that they just recommend you whatever is popular with your demographic?

Well no more. Introducing sound wave, a deep neural clustering strategy designed to give you music which matches your tastes in musical structure in style. 

Instead of relying on tags, sound wave decomposes the music into rich features relating to its actual sounds, and from there uses this to find new songs which match what you had listened to previous.

#### How it works

By using deep neural compression, we can embed large sound file, composing on millions of dimensions of data, into just 5000. This is modeled by the function:

$$ q(x; \theta) = z $$ 

This function is modeled by creating a generative model called a Variational Autoencoder. This is taken by making a generative model of encoder network q and reconstruction network f, such that:

$$ \mathop{\mathbb{E}}_{z~q_x} (-\frac{|x-f(z)|^2}{2c} -KL(q_x(z), p(z))) $$

Is maximized.

This allows us to create a rich feature reprsentation, where semantic information of the songs are stored such that similar songs exist in a space such that they are close to one another.

From there, we can compress our data set to our latent space:

$$ Z := q(X; \theta)$$ 

Perform another dimensionality reduction via PCA, and perform a nearest neightbor search to locate all nearby neighbors within the clustering.

