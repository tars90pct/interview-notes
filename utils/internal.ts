type defineComponentSetup = {
  // for data that doesn't need reactivity
  data: {
    [key: string]: any;
  };
  methods: {
    [key: string]: Function;
  };
  stores: {
    [key: string]: any;
  };
};

export function buildDefineComponentSetup<T extends defineComponentSetup, P>(
  fixedParams: T,
  params: P
): T & P {
  return { ...fixedParams, ...params };
}
