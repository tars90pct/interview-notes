export class PageMeta {
  public key = "";
  public icon: string | null = null;
  public children: PageMeta[] = [];
  public paths: string[] = [];
  public static Of(instance: any, paths: string[]): PageMeta {
    const result = Object.assign(new PageMeta(), instance);
    if (paths) {
      result.paths = [...paths];
    }
    result.children = PageMeta.OfArray(result.children, [...paths, result.key]);
    return result;
  }
  public static OfArray(instances: any[], paths: string[]): PageMeta[] {
    return instances.map((instance) => {
      return PageMeta.Of(instance, paths);
    });
  }

  public getLink(): string {
    return [...this.paths, this.key].join("/");
  }
}
