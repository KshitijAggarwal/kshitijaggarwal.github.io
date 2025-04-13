---
title: GANs
date: 2024-08-12
publish: true
website_path: deep-learning/architectures
layout: note
---

Loss: 
min_G max_D V(D, G) = E[log(D(x))] + E[log(1 - D(G(z)))]

The training process alternates between updating the Discriminator and the Generator:

a) Training the Discriminator:

- Feed real data x to D, compute D(x)
- Generate fake data G(z) by feeding random noise z to G
- Feed G(z) to D, compute D(G(z))
- Compute the discriminator loss (CE loss here): -[log(D(x)) + log(1 - D(G(z)))]
- Update D's parameters to minimize this loss

b) Training the Generator:

- Generate fake data G(z)
- Feed G(z) to D, compute D(G(z))
- Compute the generator loss: -log(D(G(z)))
- Update G's parameters to minimize this loss

```python 

for epoch in range(num_epochs):
    for real_images in dataloader:
        batch_size = real_images.size(0)
        real_images = real_images.view(batch_size, -1)

        # Train Discriminator
        d_optimizer.zero_grad()

        # Real images
        real_labels = torch.ones(batch_size, 1) # real images have label 1
        real_output = discriminator(real_images)
        d_loss_real = criterion(real_output, real_labels)

        # Fake images
        z = torch.randn(batch_size, input_dim)
        fake_images = generator(z)
        fake_labels = torch.zeros(batch_size, 1) # fake images have label 0
        fake_output = discriminator(fake_images.detach())
        # .detach() so that gradients dont flow back to generator
        d_loss_fake = criterion(fake_output, fake_labels)

        # Total discriminator loss
        d_loss = d_loss_real + d_loss_fake
        d_loss.backward()
        d_optimizer.step()

        # Train Generator
        g_optimizer.zero_grad()
        fake_output = discriminator(fake_images)
        real_labels = torch.ones(batch_size, 1) # We want the generator to produce "real" images
        g_loss = criterion(fake_output, real_labels)
        g_loss.backward()
        g_optimizer.step()

```