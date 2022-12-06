from store.models import Product

COMPARE_SESSION_ID = 'compare'


class Compare:
    def __init__(self, request):
        self.session = request.session
        compare = self.session.get(COMPARE_SESSION_ID)
        if not compare:
            compare = self.session[COMPARE_SESSION_ID] = {}
        self.compare = compare

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.compare:
            self.compare[product_id] = {'id': product_id}
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.compare:
            del self.compare[product_id]
        self.save()

    def __iter__(self):
        products_ids = self.compare.keys()
        products = Product.objects.filter(id__in=products_ids)
        for product in products:
            self.compare[str(product.id)]['product'] = product
        for data in self.compare.values():
            yield data

    def save(self):
        self.session.modified = True
