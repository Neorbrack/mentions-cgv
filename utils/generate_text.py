def generate_mentions_text(data):
    nom = data.get('nom_entreprise')
    adresse = data.get('adresse')
    statut = data.get('statut')
    email = data.get('email')
    siret = data.get('siret')

    return f"""
    <h2>Mentions légales</h2>
    <p><strong>Nom de l'entreprise :</strong> {nom}</p>
    <p><strong>Adresse :</strong> {adresse}</p>
    <p><strong>Statut juridique :</strong> {statut}</p>
    <p><strong>Numéro SIRET :</strong> {siret}</p>
    <p><strong>Email :</strong> {email}</p>
    <p><strong>Hébergement du site :</strong> Ce site est hébergé par un prestataire tiers, tel que OVH, Hostinger ou autre.</p>
    <p><strong>Responsabilité :</strong> Le propriétaire du site s'efforce de fournir des informations fiables, mais ne garantit pas leur exactitude ou leur mise à jour.</p>
    <p><strong>Propriété intellectuelle :</strong> Le contenu du site (textes, images, logo) est protégé par le droit de la propriété intellectuelle.</p>
    <p><strong>Contact :</strong> Pour toute question, vous pouvez nous écrire à l'adresse e-mail indiquée ci-dessus.</p>
    """
def generate_cgv_text(data):
    nom = data.get('nom_entreprise')

    return f"""
    <h2>Conditions Générales de Vente (CGV)</h2>
    <p><strong>1. Objet :</strong> Les présentes CGV définissent les droits et obligations entre {nom} et ses clients.</p>

    <p><strong>2. Prestations :</strong> Les services proposés sont détaillés sur le site internet ou lors de la prise de contact.</p>

    <p><strong>3. Tarifs :</strong> Les prix sont indiqués en euros. {nom} se réserve le droit de les modifier à tout moment.</p>

    <p><strong>4. Paiement :</strong> Le paiement est exigible immédiatement à la commande. Il peut s’effectuer par virement, carte bancaire ou tout autre moyen convenu.</p>

    <p><strong>5. Rétractation :</strong> Conformément à la loi, un délai de rétractation peut s’appliquer sous certaines conditions.</p>

    <p><strong>6. Responsabilité :</strong> {nom} s’engage à fournir les prestations avec professionnalisme, mais décline toute responsabilité en cas de mauvaise utilisation des livrables.</p>

    <p><strong>7. Litiges :</strong> En cas de litige, une solution amiable sera recherchée. À défaut,
"""
