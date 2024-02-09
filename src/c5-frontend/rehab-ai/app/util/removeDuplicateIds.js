//Description: This function removes duplicate property ids from the array of properties

export const removeDuplicateIds = (properties) => {
    const unique = {};
    properties.forEach(property => {
      unique[property.property_id] = property;
    });
    return Object.values(unique);
  };
  