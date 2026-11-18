/* Sobolak Technologies: shop stock.
   This is the only file you need to edit to change what is for sale.

   Each product:
     id       short unique code, goes in the email subject when someone buys
     type     'laptop' or 'desktop'            (which tab it shows under)
     art      'laptop', 'sff' or 'tower'       (which drawing to use)
     color    'black', 'graphite' or 'silver'
     name     model name
     specs    list of [label, value] rows
     grade    'A', 'B' or 'C'
     note     one honest line about condition  (optional)
     price    your price, in dollars
     ebay     what the same spec is going for on eBay (optional; leave out to hide the comparison)
     buyUrl   payment or listing link          (optional; without it the button emails you)
     sold     true to stamp it SOLD            (optional)
*/
window.SOBOLAK = {
  store: {
    // The listings below are SAMPLES so the page has something to show.
    // Replace them with real machines, then set demo to false to hide the notice.
    demo: true,

    // Where Buy buttons send people. Fill in at least the email.
    email: '',
    phone: '',

    updated: 'November 18, 2026'
  },

  products: [
    {
      id: 'T480-01',
      type: 'laptop', art: 'laptop', color: 'black',
      name: 'Lenovo ThinkPad T480',
      specs: [
        ['Processor', 'Intel Core i5-8350U'],
        ['Memory', '16 GB'],
        ['Storage', '256 GB SSD'],
        ['Screen', '14" Full HD'],
        ['System', 'Windows 11 Pro']
      ],
      grade: 'A',
      note: 'Clean lid, no dead pixels. Battery tested.',
      price: 229, ebay: 280
    },
    {
      id: 'L7490-01',
      type: 'laptop', art: 'laptop', color: 'graphite',
      name: 'Dell Latitude 7490',
      specs: [
        ['Processor', 'Intel Core i5-8350U'],
        ['Memory', '16 GB'],
        ['Storage', '256 GB SSD'],
        ['Screen', '14" Full HD'],
        ['System', 'Windows 11 Pro']
      ],
      grade: 'A',
      note: 'Light wear on the palm rest.',
      price: 209, ebay: 270
    },
    {
      id: 'O7060-01',
      type: 'desktop', art: 'sff', color: 'black',
      name: 'Dell OptiPlex 7060 SFF',
      specs: [
        ['Processor', 'Intel Core i5-8500'],
        ['Memory', '16 GB'],
        ['Storage', '256 GB NVMe SSD'],
        ['Size', 'Small form factor'],
        ['System', 'Windows 11 Pro']
      ],
      grade: 'A',
      note: 'Six cores. Quiet. Fits under a monitor.',
      price: 169, ebay: 220
    },
    {
      id: 'E840-01',
      type: 'laptop', art: 'laptop', color: 'silver',
      name: 'HP EliteBook 840 G5',
      specs: [
        ['Processor', 'Intel Core i5-8350U'],
        ['Memory', '8 GB'],
        ['Storage', '256 GB SSD'],
        ['Screen', '14" Full HD'],
        ['System', 'Windows 11 Pro']
      ],
      grade: 'B',
      note: 'Scuffs on the lid. Works the same.',
      price: 169, ebay: 220
    },
    {
      id: 'T480-02',
      type: 'laptop', art: 'laptop', color: 'black',
      name: 'Lenovo ThinkPad T480',
      specs: [
        ['Processor', 'Intel Core i5-8250U'],
        ['Memory', '16 GB'],
        ['Storage', '256 GB SSD'],
        ['Screen', '14" Full HD'],
        ['System', 'Windows 11 Pro']
      ],
      grade: 'B',
      note: 'Shiny keys, a few lid scratches.',
      price: 199, ebay: 280
    },
    {
      id: 'O7060-02',
      type: 'desktop', art: 'sff', color: 'black',
      name: 'Dell OptiPlex 7060 SFF',
      specs: [
        ['Processor', 'Intel Core i5-8500'],
        ['Memory', '16 GB'],
        ['Storage', '1 TB SSD'],
        ['Size', 'Small form factor'],
        ['System', 'Windows 11 Pro']
      ],
      grade: 'A',
      note: 'Same box, bigger drive.',
      price: 189, ebay: 238
    },
    {
      id: 'BUILD',
      type: 'desktop', art: 'tower', color: 'graphite',
      name: 'Gaming PC, built to order',
      specs: [
        ['Parts', 'Picked around your budget'],
        ['Build', 'Assembled and tested here'],
        ['System', 'Your choice']
      ],
      note: 'Tell us what you play and what you can spend.',
      priceLabel: 'Ask'
    }
  ]
};
