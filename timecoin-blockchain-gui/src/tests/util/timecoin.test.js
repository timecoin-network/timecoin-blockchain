const timecoin = require('../../util/timecoin');

describe('timecoin', () => {
  it('converts number mojo to timecoin', () => {
    const result = timecoin.mojo_to_timecoin(1000000);

    expect(result).toBe(0.000001);
  });
  it('converts string mojo to timecoin', () => {
    const result = timecoin.mojo_to_timecoin('1000000');

    expect(result).toBe(0.000001);
  });
  it('converts number mojo to timecoin string', () => {
    const result = timecoin.mojo_to_timecoin_string(1000000);

    expect(result).toBe('0.000001');
  });
  it('converts string mojo to timecoin string', () => {
    const result = timecoin.mojo_to_timecoin_string('1000000');

    expect(result).toBe('0.000001');
  });
  it('converts number timecoin to mojo', () => {
    const result = timecoin.timecoin_to_mojo(0.000001);

    expect(result).toBe(1000000);
  });
  it('converts string timecoin to mojo', () => {
    const result = timecoin.timecoin_to_mojo('0.000001');

    expect(result).toBe(1000000);
  });
  it('converts number mojo to colouredcoin', () => {
    const result = timecoin.mojo_to_colouredcoin(1000000);

    expect(result).toBe(1000);
  });
  it('converts string mojo to colouredcoin', () => {
    const result = timecoin.mojo_to_colouredcoin('1000000');

    expect(result).toBe(1000);
  });
  it('converts number mojo to colouredcoin string', () => {
    const result = timecoin.mojo_to_colouredcoin_string(1000000);

    expect(result).toBe('1,000');
  });
  it('converts string mojo to colouredcoin string', () => {
    const result = timecoin.mojo_to_colouredcoin_string('1000000');

    expect(result).toBe('1,000');
  });
  it('converts number colouredcoin to mojo', () => {
    const result = timecoin.colouredcoin_to_mojo(1000);

    expect(result).toBe(1000000);
  });
  it('converts string colouredcoin to mojo', () => {
    const result = timecoin.colouredcoin_to_mojo('1000');

    expect(result).toBe(1000000);
  });
});
